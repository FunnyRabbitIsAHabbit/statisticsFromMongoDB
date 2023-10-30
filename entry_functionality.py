"""
Entry functionality.

@Developer: Stan Ermokhin
@Version: 0.0.1
"""

import database_control
import credentials


class MainApp:
    DATABASE_APP: database_control.DatabaseControl = database_control.DatabaseControl()

    def main(self) -> None:
        self.DATABASE_APP.restore_from_dump(database_name=credentials.DATABASE_NAME,
                                            path_to_dump="sampleDB")


if __name__ == "__main__":
    app: MainApp = MainApp()
    app.main()
