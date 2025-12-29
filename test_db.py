from database import Session, engine

# Open a session
session = Session()

# Run a simple test query
result = session.execute("SELECT 1")
print(result.all())  # should print [(1,)]

# Close the session
session.close()

# Print engine to verify
print(engine)
