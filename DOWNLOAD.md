Dataset **Microscopy Malaria Dataset** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://www.dropbox.com/scl/fi/35790cveb5wc1xlumddix/microscopy-malaria-dataset-DatasetNinja.tar?rlkey=u300x0kyuookwbmyuy9mmj51g&dl=1)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Microscopy Malaria Dataset', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be downloaded here:

- [tuberculosis-phonecamera.zip](https://air.ug/static/images/downloads/tuberculosis-phonecamera.zip)
- [plasmodium-phonecamera.zip](https://air.ug/static/images/downloads/plasmodium-phonecamera.zip)
- [plasmodium-images.zip](https://air.ug/static/images/downloads/plasmodium-images.zip)
- [intestinalparasites-phonecamera.zip](https://air.ug/static/images/downloads/intestinalparasites-phonecamera.zip)
