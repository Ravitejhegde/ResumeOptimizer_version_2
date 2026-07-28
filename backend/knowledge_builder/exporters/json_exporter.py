from __future__ import annotations

import json
from pathlib import Path


class JsonExporter:

    def export(
        self,
        data: dict,
        output_directory: str,
    ) -> None:

        output = Path(output_directory)

        output.mkdir(
            parents=True,
            exist_ok=True,
        )

        for filename, content in data.items():

            file = output / f"{filename}.json"

            with file.open(
                "w",
                encoding="utf-8",
            ) as stream:

                json.dump(

                    content,

                    stream,

                    indent=4,

                    ensure_ascii=False,

                )