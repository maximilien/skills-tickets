# skills-tickets

Automate ticket response for `UserVoice` sites. Using this CLI you can automate generating `suggestions` (or ideas) for open `tickets`. You can also manage `tickets`, `suggestions`, and perform bulk operations.

# Getting started

There are two things you need to get started with the SkillsTickets CLI. From now on called CLI or `st.py`.

First, you need to get a developer or admin account on your `UserVoice` installation. When you do, you will have a series of keys that you need to save and use to use this CLI. The following section named [Credentials](##Credentials) goes into details on how to use these credentials.

Second, you need to setup your [environment](##Environment). See that section for details. However, note that you can either setup your local machine with Python3 and dependencies or better use the `Dockerfile` to create a container with all the details. You can also use one of my publish images: `dockerhub.io/drmax/skillstickers:latest`.

## Credentials

Once you have created credentials for your `UserVoice` account, you will be given the following keys: 

1. `subdomain` is the name for your `UserVoice` installation
2. `url_callback` set this to `http://localhost:4567/`
3. `api_key` this is a unique key for you
4. `api_secret` this is a unique secret key for you
5. `sso_key` this another key you need to generate in your `UserVoice` installation it perdiodically expires, so you might have to re-generate it
6. `display_name` this is the name that will be used for suggestions and tickets you create with this CLI
7. `email` this is the email you use to login to the `UserVoice` installation

You will need to keep these and use them when invoking the CLI. You can either pass each key with each invokation using the corresponding option named by the key listed above.

Or as a shortcut, you can create a `credentials.yml` file and add all your keys and info in there. Then you can pass all credentials using `--credentials=./credentials.yml`.

Create your `./credentials.yml` file with a command as follows or with your favorite editor:

```bash
cat > credentials.yml <<EOF
# Server
subdomain: cognitiveclass
url_callback: http://localhost:4567/

# APIs
api_key: [API key here, without the []]
api_secret: [API secret key here]
sso_key: [SSO key here]

# User
display_name: [display name here]
email: [email here]
EOF
```

## User guide

The following is a brief user guide for the `st.py` CLI. You can see an abreviated version of this user guide by running `./st.py --help`

```bash
➜  skills-tickets git:(master) ✗ ./st.py -h
Skills Tickets

Usage:
  st.py tickets list [options]
  st.py tickets show ID [options]
  st.py tickets delete ID [options]
  st.py tickets create TITLE BODY [options]
  st.py suggestions list [options]
  st.py suggestions show ID [options]
  st.py suggestions delete ID [options]
  st.py suggestions create FORUM_ID TITLE BODY [options]
  st.py forums list [options]
  st.py forums show ID [options]
  st.py csv verify FILE [options]
  st.py csv split FILE CLUSTER [options]

  st.py (-h | --help)
  st.py (-v | --version)

Options:
  --credentials=FILE          A YAML file with API key, user, and server options values.

  --output-file=FILE          The file path to save entries when processing CSV files.

  --subdomain=SUBDOMAIN       The subdomain name for this UserVoice installation [default: cognitiveclass].
  --url-callback=URL-CALLBACK The URL callback for this app [default: http://localhost:4567/].

  --api-key=API-KEY           The API key for the current user.
  --api-secret=API-SECRET     The API secret key for the current user.
  --sso-key=SSO-KEY           The API SSO key for the current user.

  --display-name=DISPLAY-NAME The user's name to display in messages.
  --email=EMAIL               The email for the current user.

  --show-details              Print the details of a show command, e.g., prints the list of suggestions [default: Fasle].

  --verbose                   Show all output.
  -h --help                   Show this screen.
  -v --version                Show version.
```

This lists the help for all command and options in the CLI.

### `suggestions` group

The `suggestions` command group is used to manage `UserVoice` suggestion or idea objects.

### `list` command

Usage:

`st.py suggestions list [options]`

Description:

Lists all the suggestions (or ideas). Use `--show-details` to print all the suggestions found. This can take a while.

Example:

```bash
./st.py suggestions list --credentials=./credentials.yml
Found '465' suggestions
```

### `show` command

Usage:

`st.py suggestions show ID [options]`

Description:

Displays the details for one suggestion. You need to have the unite ID for the suggestion to list it.

Example:

```bash
./st.py suggestions show 11343366 --credentials=./credentials.yml --show-details
Suggestion: 40333864 title: 'final exam : while taking it had server issues multiple times,  for CC0101EN cloud- I sent mail but no response - please respond it soon' is currently 'published'
  referrer: https://support.cognitiveclass.ai/forums/317580-general
  vote_count: 1, subscriber_count: 1, comments_count: 0, supporters_count: 1
  category: Courses, status: None, response: None
  text: final exam : while taking it had server issues multiple times,  for CC0101EN cloud- I sent mail but no response - please respond it soon - I need to get the badge for my future project
------
```

### `create` command

Usage:

`st.py suggestions create FORUM_ID TITLE BODY [options]`

Description:

Creates a suggestion. You need to find the ID of the forum where this suggestion will be created. Use the [`forums`](###forums) command to list and show forums and get their IDs. 

Example:

```bash
./st.py suggestions create 317580 "test max" "test maxim" --credentials=./credentials.yml --show-details
Created suggestion `27530678`
```

### `delete` command

Usage:

`st.py suggestions delete ID [options]`

Description:

Delete a suggestion by ID.

Example:

```bash
./st.py suggestions delete 27530678 --credentials=./credentials.yml
Deleted suggestion `27530678`
```

### `tickets` group

The `tickets` command group is used to manage `UserVoice` ticket objects.

### `list` command

Usage:

`st.py tickets list [options]`

Description:

Lists all tickets.

Example:

```bash
./st.py tickets list --credentials=./credentials.yml
Found '5711' tickets
```

### `show` command

Usage:

`st.py tickets show ID [options]`

Description:

Shows the details for a ticket passing its ID.

Example:

```bash
./st.py tickets show 457108345 --credentials=./credentials.yml
```

### `create` command

Usage:

`st.py tickets create TITLE BODY [options]`

Description:

Creates a ticket with TITLE and BODY

Example:

```bash
./st.py tickets create "my title" "text body" --credentials=./credentials.yml
Created ticket '87529309'
```

### `delete` command

Usage:

`st.py tickets delete ID [options]`

Description:

Delete a ticket by ID.

Example:

```bash
./st.py tickets delete 457108345 --credentials=./credentials.yml
Deleted ticket '457108345'
```

### `forums` group

The `forums` command group allows listing and accessing forums used to submit `suggestions`.

### `list` command

Usage:

`./st.py forums list [options]`

Description:

List the various forums. Use `--show-details` to show the ID and name for the forums.

Example:

```bash
./st.py forums list --credentials=./credentials.yml --show-details
Found '1' forums
1. ID: '317580', name: 'General'
```

### `show` command

Usage:

`st.py forums show ID [options]`

Description:

Shows the details for a forum object by ID.

Example:

```bash
/st.py forums show 317580 --credentials=./credentials.yml --show-details
Forum: '317580', name: 'General'
```

### `csv` group

The `csv` command group contains command to manipulate CSV files of tickets data to perform `--bulk` operations.

#### `verify` command

Usage: 

`st.py csv verify FILE [options]`

Description:

This command will verify a CSV file with clustered tickets data. You can use it to see the fields, find the number of entries, and also list the clusters.

Example:

```bash
./st.py csv verify ./clusters/all.csv
Entries:  found '5717' entries in './clusters/all.csv'
Keys:     found '18' keys: , id, ticket_number, name, email, subject, text, user_agent, state, assignee_name, assignee_email, user_messages_count, agent_messages_count, last_message_at, created_at, updated_at, type_field, cluster
Clusters: found '17' clusters: Miscellaneous, error, open, work, jupyter_notebook, data, file, load, run, email, time, hello, able, unable_access, python, start, jupyter_lab
```

#### `split` command

Usage: 

`st.py csv split FILE CLUSTER [options]`

Description:

This command will split a CSV file into smaller files with entries for the cluster specified.

Example:

```bash
./st.py csv split ./clusters/all.csv error --output-file=error.csv
Found '627' entries for 'error' cluster
Wrote '627' entries for cluster 'error' in file: 'error.csv'
```

## Workflows

TODO

# Developing

We welcome your contributions. You can do so by opening [issues](/issues) for features and bugs you find. Or you can submit [PRs](/pulls) when you have specific changes you would like to make. These changes can be both for source code, tests, and docs.

## Environment

This CLI uses Python 3.0 or later. Please [download Python 3](https://www.python.org/downloads/) for your particular environment to get started.

### Local

To run this CLI in your local machine. Besides Python 3 you will also need to install some dependencies. You can do so using Python's `pip` tool. Fist ensure [`pip` is installed](https://pip.pypa.io/en/stable/installing/) on your machine.

Once `pip` is installed, then install the dependencies with:

```bash
pip install docopt
pip install uservoice
pip install crypto
```

You can verify that your system is running by running the unit tests: `./hack/build.sh --test`.

Also run the CLI help with: `./st.py --help`

### Container

TODO

## Testing

The code includes both unit tests and integration tests. You can run all unit tests by invoking: `./hack/build.sh --test`.

Integration tests will require you to have [Credentials](##Credentials) for a running `UserVoice` installation in a file called `credentials.yml`. You can then invoke `./build/build.sh --e2e` to run the integration tests.

You can run both types of tests with `./hack/build.sh --all`

Once you can run all the tests. Please make your changes, add more tests, verify that all tests are passing. Create and submit a PR.

# Next steps?

The following are immediate next steps:

1. Add `--bulk` options for operations using a CSV file as the input for parameters

2. Refine the `Dockerfile` and use it in `hack/build.sh` such that all tests are run on a container to avoid and remove dependencies on local development system

3. Add missing `client_test.py` tests

4. Add more docs, particularly refining this README.md and more example workflows

5. Fix an intermitent issue with SSO login

