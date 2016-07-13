from flask_sqlalchemy import SQLAlchemy


# Global copy of SQLAlchemy. Must be created first in order to avoid
# circular dependency problems.
db = SQLAlchemy()

