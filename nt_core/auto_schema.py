from rest_framework.schemas import AutoSchema
from rest_framework.compat import coreapi, coreschema
from nt_core.exceptions import RsError
from urllib import parse


class RsSchema(AutoSchema):
    """
    使用方法：在任何APIVIEW里面

    example：
        docs = {
            'post-form': [('question_id', '试题的ID', True)],
        }
        schema = RsSchemaClass(docs=docs)

    支持的方法：get, post, delete
    支持的location：query, path, form, body

    常用的组合：
    post-form：POST 方法传输 application/json 参数
    get-query：GET 方法参数以?开始，例如：?name=zhe&age=20
    get-path： GET 方法参数在URL里面，例如：http://domain.com/zhe
    """

    def __init__(self, docs=None):
        super(RsSchema, self).__init__()
        self.docs = docs
        self.doc_fields = {}

        self.generate_doc_fields()

    def get_link(self, path, method, base_url):
        fields = self.get_path_fields(path, method)
        fields += self.get_serializer_fields(path, method)
        fields += self.get_pagination_fields(path, method)
        fields += self.get_filter_fields(path, method)

        # 把自定义的doc加进来
        if method.lower() in self.doc_fields:
            if self.doc_fields[method.lower()] is not None:
                by_name = {f.name: f for f in fields}
                for f in self.doc_fields[method.lower()]:
                    by_name[f.name] = f
                fields = list(by_name.values())

        if fields and any(
                [field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method)
        else:
            encoding = None

        description = self.get_description(path, method)

        if base_url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=parse.urljoin(base_url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=description
        )

    def generate_doc_fields(self):
        if not isinstance(self.docs, dict):
            raise RsError('DOC SCHEMA 接受参数字典')

        for method_str, doc_dt in self.docs.items():
            method_location_arr = method_str.split('-')
            if len(method_location_arr) != 2:
                raise RsError('键名格式例如： `post-form`或者`get-query`')

            method = method_location_arr[0].lower()
            if method not in ('post', 'get', 'delete'):
                raise RsError('请求方法只支持`post,get,delete`')

            location = method_location_arr[1].lower()
            if location not in ('query', 'path', 'form', 'body'):
                raise RsError(
                    '请求方法的后缀只支持`query,path,form,body`，'
                    '详情参考：http://www.django-rest-framework.org/'
                    'api-guide/schemas/#location'
                )

            for dt in doc_dt:
                try:
                    field = dt[0]
                except Exception as e:
                    continue

                try:
                    description = dt[1]
                except Exception as e:
                    description = ''

                try:
                    required = dt[2]
                except Exception as e:
                    required = False

                coreapi_field = coreapi.Field(
                    field,
                    required=required,
                    location=location,
                    schema=coreschema.String(description=description)
                )
                self.doc_fields.setdefault(
                    method, []
                ).append(coreapi_field)
