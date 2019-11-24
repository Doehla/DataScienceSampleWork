import os
import requests as req
import json
import pandas as pd

class PlanetAPI:
    '''Interface object with planet.com'''
    # Provide some default values for these properties
    satellite_id = 'REOrthoTile'
    begin_date   = "2016-07-01T00:00:00.000Z"
    end_date     = "2016-08-01T00:00:00.000Z"
    geo_json_geometry = {
        "type": "Polygon",
        "coordinates": [[[
            -122.53601074218751,
            37.71234379341038
        ],[
            -122.35404968261719,
            37.71234379341038
        ],[
            -122.35404968261719,
            37.80788523279169
        ],[
            -122.53601074218751,
            37.80788523279169
        ],[
            -122.53601074218751,
            37.71234379341038
        ]]]
    }

    def __init__(self, API_Key):
        self.API_Key = API_Key
        self.fetch_query_url_options()

    def fetch_query_url_options(self):
        '''Query the set of urls allowed by the API Key provided
        and save off in a dataframe for reference. Additionally,
        add the stats url to the set.
        '''
        # Fetch set of URLs from Planet
        result = req.get(
            'https://api.planet.com/data/v1/item-types',
            params=None,
            auth=(self.API_Key, '')
        )
        df = pd.DataFrame.from_dict(result.json()['item_types'])
        df = pd.concat([
            df['id'],
            df['_links'].apply(pd.Series).rename({'_self':'url'}, axis='columns')
        ], axis='columns').set_index('id')

        # # Add the url for stats
        # df = df.append(
        #     pd.DataFrame({
        #         'id': 'stats',
        #         'url': 'https://api.planet.com/data/v1/stats'
        #     }, index=[0]).set_index('id')
        # )
        self.urls = df.sort_index()

    def set_geo_json_geometry(self, geometry):
        self.geo_json_geometry = geometry

    def fetch_query_parameters(self):
        '''Package up the query paramaters for proper formatting.
        To change the geometry space considered: update geo_json_geometry
        To change the time interval considered: update begin_date and end_date
        '''
        query_params = {
            "type": "AndFilter",
            "config": [{
                    "type": "GeometryFilter",
                    "field_name": "geometry",
                    "config": self.geo_json_geometry
                }, {
                    "type": "DateRangeFilter",
                    "field_name": "acquired",
                    "config": {
                        "gte": self.begin_date,
                        "lte": self.end_date
                    }
                }, {
                    "type": "RangeFilter",
                    "field_name": "cloud_cover",
                    "config": {"lte": 0.5}
                }
            ]
        }
        return query_params

    def query_stats(self):
        '''Query the stats server for per day information for the
        selected satellite and composed filters'''
        result = req.post(
            'https://api.planet.com/data/v1/stats',
            auth=(self.API_Key, ''),
            json={
                "interval": "day",
                "item_types": [self.satellite_id],
                "filter": self.fetch_query_parameters()
            }
        )
        # assert (result.status_code == 200), 'Failure fetching stats data'
        return result

    def query_image_metadata(self):
        result = req.post(
            'https://api.planet.com/data/v1/quick-search',
            auth=(self.API_Key, ''),
            json={
                "item_types": [self.satellite_id],
                "filter": self.fetch_query_parameters()
            }
        )
        return result


if __name__ == '__main__':
    file_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(file_dir, 'AccessCodes', 'data.txt'), 'r') as f:
        API_Keys = json.load(f)

    oAPI = PlanetAPI(API_Keys['planet'])

    # stats = oAPI.query_stats()
    # df = pd.DataFrame.from_dict(stats.json()['buckets'])
    # print('Images contained in the selected filter: {}'.format(df['count'].sum()))

    data = oAPI.query_image_metadata()
    print(data.json())
