from unittest.mock import patch, MagicMock
from python.list_vms import list_vms


@patch("python.list_vms.compute_v1.InstancesClient")
def test_list_vms(mock_client):
    mock_instance = MagicMock()
    mock_instance.name = "project2-linux-vm"
    mock_instance.machine_type = "zones/asia-south1-a/machineTypes/e2-micro"
    mock_instance.status = "RUNNING"

    mock_interface = MagicMock()
    mock_interface.network_i_p = "10.160.0.2"
    mock_instance.network_interfaces = [mock_interface]

    mock_response = MagicMock()
    mock_response.instances = [mock_instance]

    mock_client.return_value.aggregated_list.return_value = [
        ("zones/asia-south1-a", mock_response)
    ]

    list_vms()

    mock_client.return_value.aggregated_list.assert_called_once()
