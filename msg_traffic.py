msg_card = {
        "msg_type": "interactive",
        "card": {
            "elements": [
                # {
                #     "tag": "div",
                #     "text": {
                #         "content": "{{name}}",
                #         "tag": "lark_md"
                #         }
                #     },
                {
                    "tag": "div",
                    "text": {
                        "content": "{{cpcode}}",
                        "tag": "lark_md"
                        }
                    },
                {
                    "tag": "div",
                    "text": {
                        "content": "{{cpdesc}}",
                        "tag": "lark_md"
                        }
                    },
                {
                    "tag": "div",
                    "text": {
                        "content": "{{time}}",
                        "tag": "lark_md"
                        }
                    },
                {
                    "tag": "div",
                    "text": {
                        "content": "{{traffic}}",
                        "tag": "lark_md"
                        }
                    },
                {
                    "tag": "div",
                    "text": {
                        "content": "{{threshold}}",
                        "tag": "lark_md"
                        }
                    },
                {
                    "tag": "img",
                    "img_key": "{{image}}",
                    "alt": {
                        "tag": "plain_text",
                        "content": "Traffic Image from Today's Traffic"
                    }
                    },
                {
                    "tag": "div",
                    "text": {
                        "content": "*Login into <a href='https://control.akamai.com/apps/alerting'></a> for more alert information*",
                        "tag": "lark_md"
                        }
                    }
                ],
            "header": {
                "title": {
                    "content": "{{subject}}",
                    "tag": "plain_text"
                    },
                "template": "{{color}}"
                }
            }
        }
