from google.cloud import compute_v1

def list_vms():
    project_id = "project-0435e4df-b58a-4510-a66"

    client = compute_v1.InstancesClient()

    request = compute_v1.AggregatedListInstancesRequest(
        project=project_id
    )

    for zone, response in client.aggregated_list(request=request):
        if response.instances:
            for vm in response.instances:
                print("VM Name:", vm.name)
                print("Machine Type:", vm.machine_type.split("/")[-1])
                print("Status:", vm.status)
                print("Internal IP:", vm.network_interfaces[0].network_i_p)
                print("-" * 40)

if __name__ == "__main__":
    list_vms()
