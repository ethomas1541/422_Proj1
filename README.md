# PDF Active Reading Asistant (ARA) For University of Oregon Students
_Authors_: Brian Griffith, Elijah Thomas, Kaylee Thomas, Drew Tweedale

## Use Cases

## Setting Up the ARA

This project requires the use of the NoSQL database "MongoDB". 

### Remote Server (ix)

_This project assumes that the user is a University of Oregon student/faculty member and has setup an ix-dev account. If you don't have an ix-dev account, you can create one [here](https://systems.cs.uoregon.edu/wiki/index.php?n=Help.Account)._

This step will primarily follow the instructions given on the University of Oregon Computer Science Department's [website](https://systems.cs.uoregon.edu/wiki/index.php?n=Help.ToolsMongoDB).

To set up the remote server, first open a terminal and ssh into your ix-dev account:
```
ssh <username>@ix.cs.uregon.edu
```
You will then need to install _mongoctl_. This command will prompt you to create a password for an administrative account for the database, with the username being your ix account name.
```
$ mongoctl install
This script is designed to setup an individual ngoDB server
Database password (DO NOT use your unix password):
Verify password:
The latest information about MongoDB is available on the web at http://docs.mongodb.org/v2.4 .
```


