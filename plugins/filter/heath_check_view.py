from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
    name: health_check_view
    author: Rohit Thakur (@rohitthakur2590)
    version_added: "1.0.0"
    short_description: Generate the filtered health check dict based on the provided target.
    description:
        - Generate the filtered health check dict based on the provided target.
    options:
      health_facts:
        description: Specify the health check dictionary.
        type: dict
"""

EXAMPLES = r"""
- set_fact:
   "health_facts":{
   "down_peer_count":"",
   "group_count":"",
   "neighbors":[
      {
         "msg_rcvd":3839,
         "msg_sent":3834,
         "path":{
            "memory_usage":168,
            "total_entries":2
         },
         "peer":"12.0.0.1",
         "peer_as":500,
         "peer_state":"1",
         "total_memory":776
      },
      {
         "msg_rcvd":0,
         "msg_sent":0,
         "path":{
            "memory_usage":168,
            "total_entries":2
         },
         "peer":"23.0.0.1",
         "peer_as":500,
         "peer_state":"Idle",
         "total_memory":776
      }
   ],
   "peer_count":""
}

- set_fact:
    target: {
   "name":"health_check",
   "vars":{
      "checks":[
         {
            "name":"all_neighbors_up"
         },
         {
            "name":"all_neighbors_down"
         },
         {
            "min_count":1,
            "name":"min_neighbors_up"
         }
      ]
   }
} 

- name: Get final list of parameters
  register: result
  set_fact:
    final_params: "{{ base|param_list_compare(target) }}"

# TASK [Target list] **********************************************************
# ok: [localhost] => {
#     "msg": {
#         "actionable": [
#             "2",
#             "4"
#         ],
#         "unsupported": []
#     }
# }
"""

RETURN = """
  health_check:
    description: list of unsupported params
    type: dict

"""

from ansible.errors import AnsibleFilterError

ARGSPEC_CONDITIONALS = {}


def health_check_view(*args, **kwargs):
    params = ["health_facts", "target"]
    data = dict(zip(params, args))
    data.update(kwargs)
    if len(data) < 2:
        raise AnsibleFilterError(
            "Missing either 'health facts' or 'other value in filter input,"
            "refer 'ansible.utils.pealth_check_view' filter plugin documentation for details",
        )

    health_facts = data["health_facts"]
    target = data["target"]
    health_checks = {}
    if target['name'] == 'health_check':
        vars = target.get('vars')
        if vars:
            checks = vars.get('checks')
            dn_lst = []
            un_lst = []
            for item in health_facts['neighbors']:
                if item['peer_state'] in ('Established', 1):
                    item['peer_state'] = 'Established'
                    un_lst.append(item)
                else:
                    dn_lst.append(item)
            stats = {}
            stats['up'] = len(un_lst)
            stats['down'] = len(dn_lst)
            stats['total'] = stats['up'] + stats['down']

            details = {}
            if is_present(checks, 'all_neighbors_up'):
                n_dict = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = un_lst
                    n_dict['details'] = details
                n_dict['check_status'] = get_status(stats, 'up')
                health_checks['all_neighbors_up'] = n_dict

            if is_present(checks, 'all_neighbors_down'):
                n_dict = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = dn_lst
                    n_dict['details'] = details
                n_dict['check_status'] = get_status(stats, 'down')
                health_checks['all_neighbors_down'] = n_dict

            opr = is_present(checks, 'min_neighbors_up')
            if opr:
                n_dict = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = un_lst
                    n_dict['details'] = details
                n_dict['check_status'] = get_status(stats, 'min', opr['min_count'])
                health_checks['min_neighbors_up'] = n_dict
        else:
            health_checks = health_facts
    return health_checks


def get_status(stats, check, count=None):
    if check in ('up', 'down'):
        return 'successful' if stats['total'] == stats[check] else 'failed'
    else:
        return 'successful' if count <= stats['up'] else 'failed'


def is_present(health_checks, option):
    for item in health_checks:
        if item['name'] == option:
            return item
    return None


class FilterModule(object):
    """health_check_view"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"health_check_view": health_check_view}
