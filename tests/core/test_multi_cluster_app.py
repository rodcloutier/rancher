from .common import wait_for_template_to_be_created, \
    random_str
import time


def test_multiclusterapp_create(admin_mc, admin_pc):
    client = admin_mc.client
    mcapp_name = random_str()
    catalog_name = "testcatalog"
    url = "https://github.com/mrajashree/charts.git"
    catalog1 = client.create_catalog(name=catalog_name,
                                     branch="pa2",
                                     url=url,
                                     )
    wait_for_template_to_be_created(client, catalog_name)
    tempVer = "cattle-global-data:testcatalog-wordpress-1.0.5"

    targets = [{"projectId": admin_pc.project.id}]
    print(targets)
    mcapp1 = client.create_multi_cluster_app(name=mcapp_name,
                                             templateVersionId=tempVer,
                                             targets=targets)

    wait_for_app(admin_pc, mcapp_name, 60)
    roles = mcapp1["roles"]
    # created this as admin, admin has cluster-owner and project-owner
    # roles in each cluster and project, so mcapp roles should get these
    # by default, since no roles were provided in the request
    expected_roles = ["project-owner", "cluster-owner"]
    for r in expected_roles:
        assert r in roles
    client.delete(catalog1)
    client.delete(mcapp1)


def test_multiclusterapp_create_with_members(admin_mc, admin_pc):
    client = admin_mc.client
    mcapp_name = random_str()
    catalog_name = "testcatalog"
    url = "https://github.com/mrajashree/charts.git"
    catalog1 = client.create_catalog(name=catalog_name,
                                     branch="pa2",
                                     url=url,
                                     )
    wait_for_template_to_be_created(client, catalog_name)
    tempVer = "cattle-global-data:testcatalog-wordpress-1.0.5"

    targets = [{"projectId": admin_pc.project.id}]
    print(targets)
    mcapp1 = client.create_multi_cluster_app(name=mcapp_name,
                                             templateVersionId=tempVer,
                                             targets=targets)

    wait_for_app(admin_pc, mcapp_name, 60)
    roles = mcapp1["roles"]
    # created this as admin, admin has cluster-owner and project-owner
    # roles in each cluster and project, so mcapp roles should get these
    # by default, since no roles were provided in the request
    expected_roles = ["project-owner", "cluster-owner"]
    for r in expected_roles:
        assert r in roles
    client.delete(catalog1)
    client.delete(mcapp1)


def wait_for_app(admin_pc, name, timeout=60):
    start = time.time()
    interval = 0.5
    client = admin_pc.client
    cluster_id, project_id = admin_pc.project.id.split(':')
    app_name = name+"-"+project_id
    print(app_name)
    found = False
    while not found:
        if time.time() - start > timeout:
            raise Exception('Timeout waiting for app of multiclusterapp')
        apps = client.list_app(name=app_name)
        if len(apps) > 0:
            found = True
        time.sleep(interval)
        interval *= 2
