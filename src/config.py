import toml

def load_config(file_path="conf.toml"):
    with open(file_path, "r", encoding="utf8") as f:
        return toml.load(f)
