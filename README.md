fix_kar
=======

This script will fix .kar file produced by Talend Open Studio.
If you faced a trouble with java.lang.LinkageError when using tWebService, then this script will modify kar file to avoid this exception. For more information see https://jira.talendforge.org/browse/TESB-13937

How to use it
-------------
Just call it with a name of kar file as first parameter.
You must specify path and parameters to zip/unzip and jar in first lines of script, look for SETTINGS section

Prerequisites
-------------
You need following to run this script:
 1. Python 2. It will not work with Python 3.
 2. zip or any other command line program for packing and unpacking zip archives.
 3. jar utility from JDK -> you need JDK installed.

