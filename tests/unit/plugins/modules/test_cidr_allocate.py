# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Unit test file for cidr_allocate module
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import ipaddress

from unittest import TestCase
from unittest.mock import MagicMock, patch

from ansible_collections.ansible.utils.plugins.modules.cidr_allocate import (
    CIDRAllocator,
    run_module,
)


# ---------------------------------------------------------------------------
# CIDRAllocator – Initialization & Validation
# ---------------------------------------------------------------------------


class TestCIDRAllocatorInit(TestCase):
    """Test CIDRAllocator initialization and input validation."""

    def test_valid_initialization(self):
        allocator = CIDRAllocator("10.0.0.0/8", [], 24)
        self.assertEqual(allocator.master_network, ipaddress.ip_network("10.0.0.0/8"))
        self.assertEqual(allocator.prefix_length, 24)
        self.assertEqual(allocator.used_networks, [])

    def test_valid_initialization_with_used_cidrs(self):
        allocator = CIDRAllocator(
            "10.0.0.0/8",
            ["10.0.0.0/24", "10.0.1.0/24"],
            24,
        )
        self.assertEqual(len(allocator.used_networks), 2)

    def test_invalid_master_cidr_string(self):
        with self.assertRaises(ValueError) as ctx:
            CIDRAllocator("not-a-cidr", [], 24)
        self.assertIn("Invalid master CIDR", str(ctx.exception))

    def test_prefix_length_smaller_than_master(self):
        with self.assertRaises(ValueError) as ctx:
            CIDRAllocator("10.0.0.0/16", [], 8)
        self.assertIn("smaller than master CIDR prefix length", str(ctx.exception))

    def test_prefix_length_greater_than_32(self):
        with self.assertRaises(ValueError) as ctx:
            CIDRAllocator("10.0.0.0/8", [], 33)
        self.assertIn("must be <= 32", str(ctx.exception))

    def test_invalid_used_cidr_entry(self):
        with self.assertRaises(ValueError) as ctx:
            CIDRAllocator("10.0.0.0/8", ["bad-cidr"], 24)
        self.assertIn("Invalid CIDR in used_cidrs", str(ctx.exception))

    def test_used_cidrs_outside_master_are_filtered(self):
        allocator = CIDRAllocator(
            "10.0.0.0/8",
            ["192.168.1.0/24", "10.0.0.0/24"],
            24,
        )
        self.assertEqual(len(allocator.used_networks), 1)
        self.assertEqual(
            allocator.used_networks[0],
            ipaddress.ip_network("10.0.0.0/24"),
        )

    def test_used_cidrs_sorted_by_network_address(self):
        allocator = CIDRAllocator(
            "10.0.0.0/8",
            ["10.0.2.0/24", "10.0.0.0/24", "10.0.1.0/24"],
            24,
        )
        addresses = [net.network_address for net in allocator.used_networks]
        self.assertEqual(addresses, sorted(addresses))


# ---------------------------------------------------------------------------
# CIDRAllocator – Internal methods
# ---------------------------------------------------------------------------


class TestMergeOverlappingRanges(TestCase):
    """Test the _merge_overlapping_ranges internal method."""

    def test_empty_used_networks(self):
        allocator = CIDRAllocator("10.0.0.0/8", [], 24)
        self.assertEqual(allocator._merge_overlapping_ranges(), [])

    def test_single_used_network(self):
        allocator = CIDRAllocator("10.0.0.0/8", ["10.0.0.0/24"], 24)
        merged = allocator._merge_overlapping_ranges()
        self.assertEqual(len(merged), 1)
        start = int(ipaddress.IPv4Address("10.0.0.0"))
        end = int(ipaddress.IPv4Address("10.0.0.255"))
        self.assertEqual(merged[0], (start, end))

    def test_non_overlapping_ranges(self):
        allocator = CIDRAllocator(
            "10.0.0.0/8",
            ["10.0.0.0/24", "10.0.2.0/24"],
            24,
        )
        merged = allocator._merge_overlapping_ranges()
        self.assertEqual(len(merged), 2)

    def test_overlapping_ranges_merged(self):
        allocator = CIDRAllocator(
            "10.0.0.0/8",
            ["10.0.0.0/24", "10.0.0.128/25"],
            24,
        )
        merged = allocator._merge_overlapping_ranges()
        self.assertEqual(len(merged), 1)

    def test_adjacent_ranges_merged(self):
        allocator = CIDRAllocator(
            "10.0.0.0/8",
            ["10.0.0.0/24", "10.0.1.0/24"],
            24,
        )
        merged = allocator._merge_overlapping_ranges()
        self.assertEqual(len(merged), 1)
        start = int(ipaddress.IPv4Address("10.0.0.0"))
        end = int(ipaddress.IPv4Address("10.0.1.255"))
        self.assertEqual(merged[0], (start, end))


class TestFindAvailableGaps(TestCase):
    """Test the _find_available_gaps internal method."""

    def test_no_used_cidrs_whole_master_is_gap(self):
        allocator = CIDRAllocator("10.0.0.0/24", [], 28)
        gaps = allocator._find_available_gaps()
        self.assertEqual(len(gaps), 1)
        start = int(ipaddress.IPv4Address("10.0.0.0"))
        end = int(ipaddress.IPv4Address("10.0.0.255"))
        self.assertEqual(gaps[0], (start, end))

    def test_gap_before_first_used(self):
        allocator = CIDRAllocator("10.0.0.0/24", ["10.0.0.128/25"], 28)
        gaps = allocator._find_available_gaps()
        # Should have gap from 10.0.0.0 to 10.0.0.127
        self.assertTrue(
            any(
                s == int(ipaddress.IPv4Address("10.0.0.0"))
                and e == int(ipaddress.IPv4Address("10.0.0.127"))
                for s, e in gaps
            ),
        )

    def test_gap_after_last_used(self):
        allocator = CIDRAllocator("10.0.0.0/24", ["10.0.0.0/25"], 28)
        gaps = allocator._find_available_gaps()
        self.assertTrue(
            any(
                s == int(ipaddress.IPv4Address("10.0.0.128"))
                and e == int(ipaddress.IPv4Address("10.0.0.255"))
                for s, e in gaps
            ),
        )

    def test_gap_between_used_ranges(self):
        allocator = CIDRAllocator(
            "10.0.0.0/24",
            ["10.0.0.0/26", "10.0.0.128/26"],
            28,
        )
        gaps = allocator._find_available_gaps()
        # Gap should be 10.0.0.64 - 10.0.0.127
        self.assertTrue(
            any(
                s == int(ipaddress.IPv4Address("10.0.0.64"))
                and e == int(ipaddress.IPv4Address("10.0.0.127"))
                for s, e in gaps
            ),
        )

    def test_fully_used_no_gaps(self):
        allocator = CIDRAllocator("10.0.0.0/24", ["10.0.0.0/24"], 28)
        gaps = allocator._find_available_gaps()
        self.assertEqual(gaps, [])


class TestFindAlignedCidrInGap(TestCase):
    """Test the _find_aligned_cidr_in_gap internal method."""

    def test_aligned_start(self):
        allocator = CIDRAllocator("10.0.0.0/8", [], 24)
        gap_start = int(ipaddress.IPv4Address("10.0.0.0"))
        gap_end = int(ipaddress.IPv4Address("10.0.0.255"))
        result = allocator._find_aligned_cidr_in_gap(gap_start, gap_end)
        self.assertIsNotNone(result)
        self.assertEqual(str(result), "10.0.0.0/24")

    def test_unaligned_start_finds_next_aligned(self):
        allocator = CIDRAllocator("10.0.0.0/8", [], 24)
        # Gap starts at 10.0.0.1 (not aligned for /24)
        gap_start = int(ipaddress.IPv4Address("10.0.0.1"))
        gap_end = int(ipaddress.IPv4Address("10.0.1.255"))
        result = allocator._find_aligned_cidr_in_gap(gap_start, gap_end)
        self.assertIsNotNone(result)
        self.assertEqual(str(result), "10.0.1.0/24")

    def test_gap_too_small_returns_none(self):
        allocator = CIDRAllocator("10.0.0.0/8", [], 24)
        # Gap only has 100 addresses – not enough for /24 (256)
        gap_start = int(ipaddress.IPv4Address("10.0.0.1"))
        gap_end = int(ipaddress.IPv4Address("10.0.0.100"))
        result = allocator._find_aligned_cidr_in_gap(gap_start, gap_end)
        self.assertIsNone(result)

    def test_prefix_32_single_host(self):
        allocator = CIDRAllocator("10.0.0.0/24", [], 32)
        gap_start = int(ipaddress.IPv4Address("10.0.0.5"))
        gap_end = int(ipaddress.IPv4Address("10.0.0.5"))
        result = allocator._find_aligned_cidr_in_gap(gap_start, gap_end)
        self.assertIsNotNone(result)
        self.assertEqual(str(result), "10.0.0.5/32")


# ---------------------------------------------------------------------------
# CIDRAllocator – allocate_single
# ---------------------------------------------------------------------------


class TestAllocateSingle(TestCase):
    """Test the allocate_single method."""

    def test_allocate_from_empty_master(self):
        allocator = CIDRAllocator("10.0.0.0/8", [], 24)
        result = allocator.allocate_single()
        self.assertEqual(result, "10.0.0.0/24")

    def test_allocate_avoiding_used_cidrs(self):
        allocator = CIDRAllocator("10.0.0.0/24", ["10.0.0.0/26"], 26)
        result = allocator.allocate_single()
        # Should allocate in the remaining space after 10.0.0.0/26
        allocated = ipaddress.ip_network(result)
        used = ipaddress.ip_network("10.0.0.0/26")
        self.assertFalse(allocated.overlaps(used))
        self.assertEqual(allocated.prefixlen, 26)

    def test_best_fit_prefers_smallest_gap(self):
        # Master: 10.0.0.0/24 (256 addresses)
        # Used: 10.0.0.16/28 (16 addresses at offset 16-31) and 10.0.0.64/26 (64 addresses at 64-127)
        # Gaps: [0-15] (16 addr), [32-63] (32 addr), [128-255] (128 addr)
        # Requesting /28 (16 addresses): best-fit should pick the 16-addr gap [0-15]
        allocator = CIDRAllocator(
            "10.0.0.0/24",
            ["10.0.0.16/28", "10.0.0.64/26"],
            28,
        )
        result = allocator.allocate_single()
        self.assertEqual(result, "10.0.0.0/28")

    def test_full_address_space_raises(self):
        allocator = CIDRAllocator("10.0.0.0/24", ["10.0.0.0/24"], 28)
        with self.assertRaises(ValueError) as ctx:
            allocator.allocate_single()
        self.assertIn("No available address space", str(ctx.exception))

    def test_no_aligned_block_fits_raises(self):
        # Master: 10.0.0.0/28 (16 addresses: 10.0.0.0-10.0.0.15)
        # Used: 10.0.0.0/32 (takes 10.0.0.0)
        # Gap: 10.0.0.1-10.0.0.15 (15 addresses, unaligned for /28)
        # Requesting /28 needs 16 aligned addresses; the gap starts at .1, not aligned
        allocator = CIDRAllocator("10.0.0.0/28", ["10.0.0.0/32"], 28)
        with self.assertRaises(ValueError) as ctx:
            allocator.allocate_single()
        self.assertIn("No suitable gaps found", str(ctx.exception))


# ---------------------------------------------------------------------------
# CIDRAllocator – allocate_multiple
# ---------------------------------------------------------------------------


class TestAllocateMultiple(TestCase):
    """Test the allocate_multiple method."""

    def test_allocate_count_3(self):
        allocator = CIDRAllocator("10.0.0.0/22", [], 24)
        results = allocator.allocate_multiple(3)
        self.assertEqual(len(results), 3)
        # Verify no overlaps
        networks = [ipaddress.ip_network(r) for r in results]
        for i in range(len(networks)):
            for j in range(i + 1, len(networks)):
                self.assertFalse(
                    networks[i].overlaps(networks[j]),
                    f"{networks[i]} overlaps {networks[j]}",
                )

    def test_allocate_multiple_all_within_master(self):
        master = "10.0.0.0/22"
        allocator = CIDRAllocator(master, [], 24)
        results = allocator.allocate_multiple(4)
        master_net = ipaddress.ip_network(master)
        for cidr in results:
            net = ipaddress.ip_network(cidr)
            self.assertTrue(
                net.subnet_of(master_net),
                f"{net} is not within {master_net}",
            )

    def test_partial_failure_raises(self):
        # /24 has room for exactly 1 /24
        allocator = CIDRAllocator("10.0.0.0/24", [], 24)
        with self.assertRaises(ValueError) as ctx:
            allocator.allocate_multiple(2)
        self.assertIn("Could only allocate 1 of 2", str(ctx.exception))

    def test_each_allocation_avoids_previous(self):
        allocator = CIDRAllocator("10.0.0.0/22", [], 24)
        results = allocator.allocate_multiple(3)
        # All should be distinct
        self.assertEqual(len(set(results)), 3)


# ---------------------------------------------------------------------------
# CIDRAllocator – Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases(TestCase):
    """Test edge-case scenarios."""

    def test_prefix_32_single_host_allocation(self):
        allocator = CIDRAllocator("10.0.0.0/30", [], 32)
        result = allocator.allocate_single()
        net = ipaddress.ip_network(result)
        self.assertEqual(net.prefixlen, 32)

    def test_master_equals_prefix_length(self):
        allocator = CIDRAllocator("10.0.0.0/24", [], 24)
        result = allocator.allocate_single()
        self.assertEqual(result, "10.0.0.0/24")

    def test_master_equals_prefix_length_only_one_block(self):
        allocator = CIDRAllocator("10.0.0.0/24", [], 24)
        with self.assertRaises(ValueError):
            allocator.allocate_multiple(2)

    def test_used_cidrs_outside_master_ignored(self):
        allocator = CIDRAllocator(
            "10.0.0.0/24",
            ["192.168.0.0/16", "172.16.0.0/12"],
            28,
        )
        # No used_networks should be stored since none overlap
        self.assertEqual(len(allocator.used_networks), 0)
        result = allocator.allocate_single()
        self.assertEqual(result, "10.0.0.0/28")

    def test_overlapping_used_cidrs_merged(self):
        # 10.0.0.0/25 and 10.0.0.0/26 overlap (the /26 is inside the /25)
        allocator = CIDRAllocator(
            "10.0.0.0/24",
            ["10.0.0.0/25", "10.0.0.0/26"],
            25,
        )
        merged = allocator._merge_overlapping_ranges()
        self.assertEqual(len(merged), 1)
        # The merged range should cover the entire /25
        self.assertEqual(
            merged[0][0],
            int(ipaddress.IPv4Address("10.0.0.0")),
        )
        self.assertEqual(
            merged[0][1],
            int(ipaddress.IPv4Address("10.0.0.127")),
        )

    def test_allocate_multiple_prefix_32(self):
        allocator = CIDRAllocator("10.0.0.0/30", [], 32)
        results = allocator.allocate_multiple(4)
        self.assertEqual(len(results), 4)
        self.assertEqual(len(set(results)), 4)


# ---------------------------------------------------------------------------
# run_module – integration with AnsibleModule
# ---------------------------------------------------------------------------


class TestRunModule(TestCase):
    """Test the run_module function via AnsibleModule mocking."""

    @patch(
        "ansible_collections.ansible.utils.plugins.modules.cidr_allocate.AnsibleModule",
    )
    def test_single_allocation_success(self, mock_module_cls):
        mock_module = MagicMock()
        mock_module_cls.return_value = mock_module
        mock_module.params = {
            "master_cidr": "10.0.0.0/8",
            "used_cidrs": [],
            "prefix_length": 24,
            "count": 1,
        }
        mock_module.check_mode = False

        run_module()

        mock_module.exit_json.assert_called_once()
        call_kwargs = mock_module.exit_json.call_args[1]
        self.assertEqual(call_kwargs["changed"], False)
        self.assertEqual(call_kwargs["allocated_cidrs"], ["10.0.0.0/24"])
        self.assertEqual(call_kwargs["count"], 1)

    @patch(
        "ansible_collections.ansible.utils.plugins.modules.cidr_allocate.AnsibleModule",
    )
    def test_multiple_allocation_success(self, mock_module_cls):
        mock_module = MagicMock()
        mock_module_cls.return_value = mock_module
        mock_module.params = {
            "master_cidr": "10.0.0.0/22",
            "used_cidrs": [],
            "prefix_length": 24,
            "count": 3,
        }
        mock_module.check_mode = False

        run_module()

        mock_module.exit_json.assert_called_once()
        call_kwargs = mock_module.exit_json.call_args[1]
        self.assertEqual(call_kwargs["count"], 3)
        self.assertEqual(len(call_kwargs["allocated_cidrs"]), 3)

    @patch(
        "ansible_collections.ansible.utils.plugins.modules.cidr_allocate.AnsibleModule",
    )
    def test_invalid_master_cidr_fails(self, mock_module_cls):
        mock_module = MagicMock()
        mock_module_cls.return_value = mock_module
        mock_module.params = {
            "master_cidr": "not-valid",
            "used_cidrs": [],
            "prefix_length": 24,
            "count": 1,
        }
        mock_module.check_mode = False

        run_module()

        mock_module.fail_json.assert_called_once()
        fail_msg = mock_module.fail_json.call_args[1]["msg"]
        self.assertIn("Invalid master CIDR", fail_msg)

    @patch(
        "ansible_collections.ansible.utils.plugins.modules.cidr_allocate.AnsibleModule",
    )
    def test_count_less_than_1_fails(self, mock_module_cls):
        mock_module = MagicMock()
        mock_module_cls.return_value = mock_module
        mock_module.params = {
            "master_cidr": "10.0.0.0/8",
            "used_cidrs": [],
            "prefix_length": 24,
            "count": 0,
        }
        mock_module.check_mode = False

        run_module()

        mock_module.fail_json.assert_called_once()
        fail_msg = mock_module.fail_json.call_args[1]["msg"]
        self.assertIn("count must be at least 1", fail_msg)

    @patch(
        "ansible_collections.ansible.utils.plugins.modules.cidr_allocate.AnsibleModule",
    )
    def test_exhausted_space_fails(self, mock_module_cls):
        mock_module = MagicMock()
        mock_module_cls.return_value = mock_module
        mock_module.params = {
            "master_cidr": "10.0.0.0/24",
            "used_cidrs": ["10.0.0.0/24"],
            "prefix_length": 28,
            "count": 1,
        }
        mock_module.check_mode = False

        run_module()

        mock_module.fail_json.assert_called_once()

    @patch(
        "ansible_collections.ansible.utils.plugins.modules.cidr_allocate.AnsibleModule",
    )
    def test_allocation_with_used_cidrs(self, mock_module_cls):
        mock_module = MagicMock()
        mock_module_cls.return_value = mock_module
        mock_module.params = {
            "master_cidr": "10.0.0.0/24",
            "used_cidrs": ["10.0.0.0/26"],
            "prefix_length": 26,
            "count": 1,
        }
        mock_module.check_mode = False

        run_module()

        mock_module.exit_json.assert_called_once()
        call_kwargs = mock_module.exit_json.call_args[1]
        allocated = ipaddress.ip_network(call_kwargs["allocated_cidrs"][0])
        used = ipaddress.ip_network("10.0.0.0/26")
        self.assertFalse(allocated.overlaps(used))
