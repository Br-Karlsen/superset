

```bash

superset db upgrade;
superset fab create-admin;
superset load_examples;
superset init;
superset run -p 8088 --with-threads --reload --debugger;

```
