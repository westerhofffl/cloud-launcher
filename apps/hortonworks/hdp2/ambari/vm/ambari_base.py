# Copyright 2014 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
################################################################################
#
# Ambari server + agent deployment.
#
################################################################################

from gce import *

def AmbariCluster(
    numAgents=4,
    agentMachineType='n1-standard-4',
    agentDiskSizeGb=500,
    agentInitScript=None,
    agentSourceImage=None,
    serverMachineType='n1-standard-1',
    serverInitScript=None,
    serverSourceImage=None,
    sourceImage=None):
  if agentSourceImage is None:
    agentSourceImage = sourceImage
  if serverSourceImage is None:
    serverSourceImage = sourceImage

  server = Compute.instance(
      name='ambari-server',
      machineType=serverMachineType,
      disks=[
        Disk.boot(
          autoDelete=true,
          initializeParams=Disk.initializeParams(
            sourceImage=serverSourceImage,
          ),
        ),
      ],
      metadata=Metadata.create(
        items=[
          Metadata.startupScript(serverInitScript),
        ],
      ),
    )

  agents = [Compute.instance(
      name='ambari-agent-%d' % i,
      machineType=agentMachineType,
      disks=[
        Disk.boot(
          autoDelete=true,
          initializeParams=Disk.initializeParams(
            sourceImage=agentSourceImage,
            diskSizeGb=agentDiskSizeGb,
          ),
        ),
      ],
      metadata=Metadata.create(
        items=[
          Metadata.item('ambari-server', server.name),
          Metadata.startupScript(agentInitScript),
        ],
      ),
    ) for i in range(0, numAgents)
  ]

  return [server] + agents
