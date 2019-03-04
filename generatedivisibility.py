import sys
import string
# If the user has pyperclip, we can copy to clipboard,
# But don't make a big deal about it
try:
    import pyperclip
except:
    pass

# Convert to base 26, a-z, aa-az, ba-bz, etc for capture groups
def get_name(number):
    name = ''
    while number:
        number, q = divmod(number, 26)
        name += string.ascii_uppercase[q]
    return name or 'A'


# Get the digit for a given number, 0-9, A-Z, a-z.
def get_digit(number):
    return (string.digits + string.ascii_uppercase + string.ascii_lowercase)[number]


# Grab our basic options: base of number, divisor, and whether to output a DFA file
# Or a recursive regex. A DFA file will be converted to a regex in JFLAP
# JFLAP regexes are extremely large since they collapse states
# Recursive regexes rely on features that might not be in every engine, but are significantly smaller.

print('Welcome to the divisibility regex generator wizard!')

choice = int(input('\n\nYou can either generate a JFLAP DFA file for conversion into a regex in the JFLAP toolkit,'
                   '\nor you cangenerate a simple regex using Ruby or Python recursion syntax.\n\n'
                   'JFLAP regexes will be much larger but will be supported in regex engines\n'
                   'without recursion. Recursive regexes will (obviously) require a regex engine\ncapable of recursion.'
                   ' JFLAP regexes will also require all "+" chars to be replaced with "|" chars,\n'
                   'since DFA regexes use a different syntax than programmer regexes.\n\n'
                   '1. JFLAP file\n'
                   '2. Recursive regex\n>>>'))

# Deny improper choice
if choice not in [1, 2]:
    print('Improper choice!')
    sys.exit()

base = int(input('\nPlease enter the base you want to parse\n>>>').strip('\n\t '))
divisor = int(input('\nPlease enter the divisor you want to parse:\n>>>').strip('\n\t '))


if choice == 1:
    fa = ''

    fa += '''<structure>
    <type>fa</type>
    <automaton>'''

    for state in range(divisor):
        fa += '<state id="%s" name="q%s">' % (state, state)
        fa += '<x>0</x><y>0</y>'
        if state == 0:
            fa += '<final/><initial/>'
        fa += '</state>'

    for state in range(divisor):
        for digit in range(base):
            fa += '<transition>'
            fa += '<from>%s</from>' % state
            fa += '<to>%s</to>' % ((state * base + digit) % divisor)
            fa += '<read>%s</read>' % digit
            fa += '</transition>'

    fa += '</automaton></structure>'

    with open(input('\nPlease enter your desired filename eg. divisible_by_9\n>>>') + '.jff', 'w') as f:
        f.write(fa)

else:
    format = int(input('Which format of recursion and named group you like to generate?\n'
                       '1. Python format: (?&NAME)\n'
                       '2. Ruby format: (\\g<NAME>)\n'
                       'Note: PCRE supports both\n'
                       'Note: Default re module for Python does not support '
                       'recursion or DEFINE, please use regex module\n'
                       '>>>'))

    if format not in [1, 2]:
        print('Improper choice!')
        sys.exit()

    # Don't match empty strings or middle of strings
    regex = '(?!$|0[^0]$)(?<!\\d)'

    # Python uses DEFINE, Ruby will use atomic group
    regex += '(?(DEFINE)' if format == 1 else '(?>'

    states = {}

    # Generate out states table
    for state in range(divisor):
        states[state] = {}
        for digit in range(base):
            try:
                states[state][(state * base + digit) % divisor] += get_digit(digit)
            except:
                states[state][(state * base + digit) % divisor] = get_digit(digit)

    # For every state except our state 0, print out the state.
    # State 0 comes last as it is final state and thus has to match.

    # Can't use keyword 'from'
    for fromstate in filter(lambda x: x != 0, states.keys()):
        # Use Python or .NET syntax for named group.
        # These are the two standards as they came first

        if format == 1:
            regex += '(?P<%s>' % get_name(fromstate)
        else:
            regex += '(|(?<%s>' % get_name(fromstate)

        # Generate a table of options for that state
        final_state_options = []
        for to in states[fromstate]:
            #
            final_state_options.append(
                ('%s(?&%s)' if format == 1 else '%s\\g<%s>')  # Use the proper recursion format
                % (
                    # If we have one option, just print it, otherwise use brackets syntax
                    states[fromstate][to] if len(states[fromstate][to]) == 1 else '[' + states[fromstate][to] + ']',
                    # Get the alphabetical name for the to state
                    get_name(to)
                )
            )

        regex += '|'.join(final_state_options)
        regex += ')'
        # If we're using PCRE, we need to close an extra parenthesis and put alternations between state definitions
        if format == 2:
            regex += ')'
            """
        # Only put an alternation if we are not the last state
        if fromstate != divisor - 1 and format == 2:
            regex += '|'
            """


    regex += ')'

    # Again use proper named group format, Python mysteriously breaks if the \b is included.
    regex += '(?P<A>$|' if format == 1 else '(?<A>$|\\b|'


    final_state_options = []

    for to in states[0]:
        # Same as other states, just this is the one that actually matches
        final_state_options.append(('%s(?&%s)' if format == 1 else '%s\\g<%s>') % (
            states[0][to] if len(states[0][to]) == 1 else '[' + states[0][to] + ']',
            get_name(to)
        ))

    # Join the final state options and close the parenthesis
    regex += '|'.join(final_state_options) + ')'

    # Print the regex and attempt to copy to clipboard if the user has pyperclip
    try:
        pyperclip.copy(regex)
    except:
        pass
    print(regex)
    # Wait for user input before closing.
    input()
