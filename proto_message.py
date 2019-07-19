import proto


class UrlHTML(proto.Message):
    url = proto.Field(proto.STRING, number=1)
    raw = proto.Field(proto.STRING, number=2)
