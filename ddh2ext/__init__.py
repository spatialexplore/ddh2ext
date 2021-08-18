
import requests
import pandas as pd
from .exceptions import *

class DDH2():

	def __init__(self):
		self.host = "https://datacatalogapi.worldbank.org"

	def get_endpoint(self, endpoint):
		return '/'.join([self.host, endpoint])

	def get(self, endpoint, params=None):
		'''Send a GET request
		
		Arguments:
			endpoint:		the endpoint (e.g., "ddhxext/search")
			
			params:			query parameters

		Returns:
			a Response object (from the requests package)
		'''

		return requests.get(self.get_endpoint(endpoint), params=params)

	def search(self, qterm=None, qname='Dataset', filter=None, max=None, pageSize=50):
		'''Search for dataset(s)

		Arguments:
			qterm:		Query term

			qname:		Type of query. Values are Dataset, DataResource, Indicator

			filter:		Search filter - Azure search filter string

			max:		Maximum number of pages of search results to return

			pageSize:	Number of results per page
		'''

		def fetch(page):
			params = {"qname": qname}
			if qterm:
				params["qterm"] = qterm
			else:
				params["qterm"] = "*"
			if filter:
				params["$filter"] = filter
			params["$top"] = pageSize
			params["$skip"] = pageSize * (page)
			response = self.get("ddhxext/Search", params)
			if response.status_code != 200:
				raise DDH2Exception(response)
			return response.json()

		pageMax = None
		pageNum = n = 0
		while pageMax is None or pageNum * pageSize <= pageMax:
			batch = fetch(pageNum)
			pageMax = batch['Response']['@odata.count']
			for row in batch['Response']['value']:
				yield row

				n += 1

			pageNum += 1

			if max and pageNum >= max:
				break

	def get_tagged(self, tags=None):
		'''Get dataset(s) tagged with any of a list of keywords

		Arguments:
			tags:		List of keywords

        Returns:
            a pandas DataFrame of datasets
		'''
		if tags:
			tags_str = ",".join(tags)
			filter = "keywords/any(k: search.in(k/name, '{0}'))".format(tags_str)
			return pd.DataFrame(self.search(filter=filter))

	def get_dataset(self, id, version=None):
		'''Get a dataset by id

		Arguments:
			id:			the dataset's unique id
			version:    id of the specific version to get. If None, latest version is returned

		Returns:
			a Dataset object in JSON format
		'''
		response = None
		params = {'dataset_unique_id': id}
		if version:
			params['version_id'] = version
		response = self.get('ddhxext/DatasetView', params)
		if response.status_code != 200:
			raise DDH2Exception(response)
		return response.json()

	def get_datasets_list(self, pageSize=100):
		'''Get a list of all datasets

		Arguments:
			pageSize:		number of datasets per page

		Returns:
			a list of dataset objects in JSON format

		'''
		def fetch(skip):
			params = {'skip': skip}
			params['top'] = pageSize
			response = self.get("ddhxext/DatasetList", params)
			if response.status_code != 200:
				raise DDH2Exception(response)
			return response.json()

		pageMax = None
		pageNum = n = 0
		while pageMax is None or pageNum <= pageMax:
			batch = fetch(pageNum)
			pageMax = batch['count']
			for row in batch['data']:
				yield row
				n += 1

			pageNum += n

	def get_resource(self, id):
		'''Get a resource by id

		Arguments:
			id:			the unique id of the resource

		Returns:
			a Resource object in JSON format
		'''
		params = {'resource_unique_id': id}

		response = self.get('ddhxext/ResourceView', params)
		if response.status_code != 200:
			raise DDH2Exception(response)
		return response.json()

	def download_resource(self, id, version=None):
		'''Download a resource file by id

		Arguments:
			id:			the unique id of the resource
			version:	version of the dataset (optional)

		Returns:
			downloads the resource file
		'''
		params = {'resource_unique_id': id}
		if version:
			params['version_id'] = version
		else:
			params['version_id'] = ''

		response = self.get('ddhxext/ResourceDownload', params)
		if response.status_code != 200:
			raise DDH2Exception(response)
		return response.json()

	def get_resource_preview(self, id, version=None, filter=None, rows=100):
		'''Get a preview of the contents of a resource by id. This is for CSV and structured Excel
		   resource files only.

		Arguments:
			id:			the unique id of the resource
			version:	version of the dataset (optional)
			filter:		filter string for restricting the data returned (optional)
			rows:		number of rows to return (optional - default 100)

		Returns:
			the first {rows} rows of data in the resource file in JSON format
		'''
		params = {'resource_unique_id': id}
		if version:
			params['version_id'] = version
		else:
			params['version_id'] = ''
		if filter:
			params['filter'] = filter
		params['rowLimit'] = rows

		response = self.get('ddhxext/ResourceFileData', params)
		if response.status_code != 200:
			raise DDH2Exception(response)
		return response.json()

