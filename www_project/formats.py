import dicttoxml
from import_export.formats.base_formats import TextFormat


class XML(TextFormat):
    def get_title(self):
        return 'xml'

    def is_binary(self):
        """
        Returns if this format is binary.
        """
        return False

    def get_extension(self):
        """
        Returns extension for this format files.
        """
        return ".xml"

    def get_content_type(self):
        return 'application/xml'

    def can_import(self):
        return False

    def can_export(self):
        return True

    def export_data(self, dataset, **kwargs):
        """
        Returns format representation for given dataset.
        """
        kwargs.setdefault('attr_type', False)
        return dicttoxml.dicttoxml(dataset.dict)

class Format:
    def get_title(self):
        return type(self)

    def create_dataset(self, in_stream):
        """
        Create dataset from given string.
        """
        raise NotImplementedError()

    def export_data(self, dataset, escape_output=False, **kwargs):
        """
        Returns format representation for given dataset.
        """
        raise NotImplementedError()

    def is_binary(self):
        """
        Returns if this format is binary.
        """
        return True

    def get_read_mode(self):
        """
        Returns mode for opening files.
        """
        return 'rb'

    def get_extension(self):
        """
        Returns extension for this format files.
        """
        return ""

    def get_content_type(self):
        # For content types see
        # https://www.iana.org/assignments/media-types/media-types.xhtml
        return 'application/octet-stream'

    @classmethod
    def is_available(cls):
        return True

    def can_import(self):
        return False

    def can_export(self):
        return False


class TablibFormat(Format):
    TABLIB_MODULE = None
    CONTENT_TYPE = 'application/octet-stream'

    def __init__(self, encoding=None):
        self.encoding = encoding

    def get_format(self):
        """
        Import and returns tablib module.
        """
        if not self.TABLIB_MODULE:
            raise AttributeError("TABLIB_MODULE must be defined")
        key = self.TABLIB_MODULE.split('.')[-1].replace('_', '')
        return registry.get_format(key)

    @classmethod
    def is_available(cls):
        try:
            cls().get_format()
        except (tablib.core.UnsupportedFormat, ImportError):
            return False
        return True

    def get_title(self):
        return self.get_format().title

    def create_dataset(self, in_stream, **kwargs):
        return tablib.import_set(in_stream, format=self.get_title(), **kwargs)

    def export_data(self, dataset, **kwargs):
        # remove the deprecated `escape_output` param if present
        kwargs.pop("escape_output", None)
        if kwargs.pop("escape_html", None):
            self._escape_html(dataset)
        if kwargs.pop("escape_formulae", None):
            self._escape_formulae(dataset)
        return dataset.export(self.get_title(), **kwargs)

    def get_extension(self):
        return self.get_format().extensions[0]

    def get_content_type(self):
        return self.CONTENT_TYPE

    def can_import(self):
        return hasattr(self.get_format(), 'import_set')

    def can_export(self):
        return hasattr(self.get_format(), 'export_set')

    def _escape_html(self, dataset):
        for _ in dataset:
            row = dataset.lpop()
            row = [html.escape(str(cell)) for cell in row]
            dataset.append(row)

    def _escape_formulae(self, dataset):
        def _do_escape(s):
            return s.replace("=", "", 1) if s.startswith("=") else s

        for _ in dataset:
            row = dataset.lpop()
            row = [_do_escape(str(cell)) for cell in row]
            dataset.append(row)


class TextFormat(TablibFormat):

    def create_dataset(self, in_stream, **kwargs):
        if isinstance(in_stream, bytes) and self.encoding:
            in_stream = in_stream.decode(self.encoding)
        return super().create_dataset(in_stream, **kwargs)

    def get_read_mode(self):
        return 'r'

    def is_binary(self):
        return False