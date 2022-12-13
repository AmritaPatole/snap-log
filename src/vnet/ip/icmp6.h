/*
 * Copyright (c) 2015 Cisco and/or its affiliates.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at:
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef included_vnet_icmp6_h
#define included_vnet_icmp6_h

#include <vnet/ip/icmp46_packet.h>

typedef struct
{
  u8 packet_data[64];
} icmp6_input_trace_t;

format_function_t format_icmp6_input_trace;
void icmp6_register_type (vlib_main_t * vm, icmp6_type_t type,
			  u32 node_index);
void icmp6_error_set_vnet_buffer (vlib_buffer_t * b, u8 type, u8 code,
				  u32 data);

extern vlib_node_registration_t ip6_icmp_input_node;

#endif /* included_vnet_icmp6_h */



/*
 * fd.io coding-style-patch-verification: ON
 *
 * Local Variables:
 * eval: (c-set-style "gnu")
 * End:
 */
