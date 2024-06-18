from fastapi import FastAPI


class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, version="0.1.0")


app = App()
