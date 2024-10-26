from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('menuResto', '0001_initial'),  # Replace with your actual previous migration
    ]

    operations = [
        # First create a new table with the structure we want
        migrations.RunSQL(
            sql="""
            CREATE TABLE menuResto_tag_menus_new (
                tag_id INTEGER NOT NULL REFERENCES menuResto_tag(id),
                menu_id INTEGER NOT NULL REFERENCES menuResto_menu(id),
                PRIMARY KEY(tag_id, menu_id)
            );
            
            -- Copy data from old table to new table
            INSERT INTO menuResto_tag_menus_new (tag_id, menu_id)
            SELECT tag_id, menu_id FROM menuResto_tag_menus;
            
            -- Drop the old table
            DROP TABLE menuResto_tag_menus;
            
            -- Rename the new table to the original name
            ALTER TABLE menuResto_tag_menus_new RENAME TO menuResto_tag_menus;
            """,
            reverse_sql="""
            CREATE TABLE menuResto_tag_menus_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag_id INTEGER NOT NULL REFERENCES menuResto_tag(id),
                menu_id INTEGER NOT NULL REFERENCES menuResto_menu(id)
            );
            
            INSERT INTO menuResto_tag_menus_new (tag_id, menu_id)
            SELECT tag_id, menu_id FROM menuResto_tag_menus;
            
            DROP TABLE menuResto_tag_menus;
            
            ALTER TABLE menuResto_tag_menus_new RENAME TO menuResto_tag_menus;
            """
        ),
    ]