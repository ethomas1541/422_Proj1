# PDF Active Reading Asistant (ARA) For University of Oregon Students
_Authors_: Brian Griffith, Elijah Thomas, Kaylee Thomas, Drew Tweedale

## Use Cases

## Setting Up the ARA

This project requires the use of the relational database MySQL. We'll provide instructions on how to set up the MySQL instance on the University of Oregon webservers, as well as instructions for installing the required drivers to run the application.

### Remote Server (ix)

_This project assumes that the user is a University of Oregon student/faculty member and has setup an ix-dev account. If you don't have an ix-dev account, you can create one [here](https://systems.cs.uoregon.edu/wiki/index.php?n=Help.Account)._

This step will primarily follow the instructions given on the University of Oregon Computer Science Department's [website](https://systems.cs.uoregon.edu/wiki/index.php?n=Help.ToolsMysql).

#### 1) Connecting to ix and Installing MySQLCTL
To set up the remote server, first open a terminal and ssh into your ix-dev account:
```
ssh <username>@ix.cs.uregon.edu
```
You will then need to install _mysqlctl_ by entering the command `mysqlctl install`. It will then ask you for a password. This is your password for MySQL, not your CS unix account: it doesn't need to be the same. **Remember this password**.

#### 2) Modify .my.cnf File

Run `mysqlctl start` and then `mysqlctl stop`. You now can edit your .my.cnf file (this file is hidden, so you might need to enter the command `ls -a` to locate it). Edit this file using `emacs` or `vim`, and make the following changes:
* Comment out the line that says `skip-innodb`.
* Comment out the line that says `default-storage-engine=myisam`.
* Take note of your port number.

Now restart your MySQL instance (`mysqlctl start`).

#### 3) Creating your Remote User

You will need to create a user that can access your MySQL instance remotely. To do so:
* Run MySQL from the command line, using `mysql -p` _this will ask for your MySQL password from the initial step_
* Enter the command: `create user 'pparker'@'%' identified by 'password';`, with _pparker_ and _password_ swapped for your username and password.
* Enter: `grant all privileges on *.* to 'pparker'@'%' with grant option;`
* Exit MySQL using `quit` or `exit`.

You now have your username, password, and port number. To check the status of your MySQL instance, enter `mysqlctl status`.

### Configuring the ARA

#### MySQL.Connector

You will need to install the `mysql.connector` package to run this program. To do so, make sure you have `pip` or `pip3` installed, depending on your python version. To install `mysql.connector`, run the command:
```
pip install mysql-connector-python
```
_Exchange pip for pip3 if needed_

#### Admin Setup

To configure the database, first select to the _admin_ user. This user has a `Server Setup` option, where the user can configure the server connection properties: `host, port, username, and password`. These settings are what we created in the previous step.






