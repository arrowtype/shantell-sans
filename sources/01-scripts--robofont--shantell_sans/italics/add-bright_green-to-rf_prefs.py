from mojo.UI import getDefault, setDefault, preferencesChanged

# get current value
marks = getDefault("markColors")
print(f"previous value: {marks}")

marks = list(marks) + [((0.67, 0.95, 0.38, 1.0), "bright green")]

# set a new value
setDefault("markColors", tuple(marks))
marks = getDefault("markColors")
print(f"new value: {marks}")

# tell the app that preferences were changed
preferencesChanged()