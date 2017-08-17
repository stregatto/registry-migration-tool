registry-migration-tool
=======================

This tool permit to read deployments from a kube cluster, retrieve images from registry and push that image on another registry

if your source registry uses auth auth you have to proper setup envar to pull images
If your destination registry uses auth you have to proper setup envar for every organization.

Organization is the "folder" after the name of source registry

*E.G.*
 _image_: gcr.io/google_containers/kube-state-metrics:v0.2.0
 _organization_: google_containers

The envars are in the format DT_[DESTINATION|SOURCE]_${organization_uppercase}_[USERNAME|TOKEN]

*E.G.*

```bash
export DT_DESTINATION_REGISTRY_APPLICATION_USERNAME='application+robotaccount'
export DT_DESTINATION_REGISTRY_APPLICATION_TOKEN='AAAABBBBCCCCDDDDEEEEFFF'
```

Example
-------

```bash
export DT_DESTINATION_REGISTRY_APPLICATION_USERNAME='application+robotaccount'
export DT_DESTINATION_REGISTRY_APPLICATION_TOKEN='AAAABBBBCCCCDDDDEEEEFFF'
python ./registrytool.py -r registry-destination.mycompany.com:5000
```
