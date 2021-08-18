# DDH2ext

DDH2ext provides a python interface to the World Bank's forthcoming DDH2 platform. This
is designed for external use by the public.

## Installation ##

`pip install git+git://github.com/spatialexplore/ddh2ext`

or

`pip install git+https://github.com/spatialexplore/ddh2ext`

You can also download this repository as a ZIP archive and install like this:

`pip install Downloads\ddh2ext-master.zip`

## Requirements ##

DDH2ext requires the requests module. 

## Use ##

````
# ddh uses the requests module and returns the same results as requests.get
response = ddh2.get('ddhxext/DatasetView)
print(response.json())
````
