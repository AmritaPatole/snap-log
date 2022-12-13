/*
 * Copyright (c) 2020 Cisco and/or its affiliates.
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

#include <vnet/vnet.h>
#include <perfmon/perfmon.h>
#include <perfmon/intel/core.h>

static u8 *
format_inst_and_clock (u8 *s, va_list *args)
{
  perfmon_node_stats_t *ns = va_arg (*args, perfmon_node_stats_t *);
  int row = va_arg (*args, int);

  switch (row)
    {
    case 0:
      s = format (s, "%lu", ns->n_calls);
      break;
    case 1:
      s = format (s, "%lu", ns->n_packets);
      break;
    case 2:
      s = format (s, "%.2f", (f64) ns->n_packets / ns->n_calls);
      break;
    case 3:
      s = format (s, "%.2f", (f64) ns->value[1] / ns->n_packets);
      break;
    case 4:
      s = format (s, "%.2f", (f64) ns->value[0] / ns->n_packets);
      break;
    case 5:
      s = format (s, "%.2f", (f64) ns->value[0] / ns->value[1]);
      break;
    }
  return s;
}

PERFMON_REGISTER_BUNDLE (inst_and_clock) = {
  .name = "inst-and-clock",
  .description = "instructions/packet, cycles/packet and IPC",
  .source = "intel-core",
  .type = PERFMON_BUNDLE_TYPE_NODE,
  .events[0] = INTEL_CORE_E_INST_RETIRED_ANY_P,
  .events[1] = INTEL_CORE_E_CPU_CLK_UNHALTED_THREAD_P,
  .events[2] = INTEL_CORE_E_CPU_CLK_UNHALTED_REF_TSC,
  .n_events = 3,
  .format_fn = format_inst_and_clock,
  .column_headers = PERFMON_STRINGS ("Calls", "Packets", "Packets/Call",
				     "Clocks/Packet", "Instructions/Packet",
				     "IPC"),
};
