This is the engineering challenge for the data engineering roles at [The
Atlantic](https://www.theatlantic.com).  Please follow the instructions
carefully.

## Background
The following is a hypothetical situation that would require some engineering
and database design.  Imagine we have an external ecommerce vendor that
handles online and phone based ordering of our subscription products.  We'd
like to have a copy of our subscriber records in an internal database that we
can query directly, and our vendor is only willing to provide daily
extractions from their database of the records that have changed in the last
24 hours.  Imagine the vendor has limited technical resources, and would like
to upload the file containing new/updated records manually to a website we
provide.

## Deliverable
Create a web application that allows a file to be uploaded via a form
submission and then parses the uploaded file and inserts / updates records in
a relational database.  You may use any language, framework, or tools that
you'd like, as long as they are free and open source and can be run on either
a Linux or Mac OS X machine.  Your web application does not need
authentication or authorization capabilities.  Assume that uploaded files
won't exceed 3 MB in size.  Uploaded files will have tab delimited fields and
records will be separated by newline characters.  Each line will have the
following fields in the given order (an example input file can be found
[here](https://pastebin.com/raw/ZKWDLhxw)):

1. Customer id (an integer)
1. Customer first name
1. Customer last name
1. Customer street address (assume US addresses only)
1. Customer state (assume US addresses only)
1. Customer zip code  (assume US addresses only)
1. Change in purchase status - this will be either 'new' or 'canceled'
1. Product id for purchase (an integer)
1. Product name (a string, not longer than 100 characters)
1. Product purchase amount (in US dollars)
1. Date and time in ISO8601 format, i.e. 2007-04-05T14:30Z

Please include instructions describing the process to setup/install any
prerequisite software, initialize the relational database, and run the web
application.

## Submission
Please email [data@theatlantic.com](mailto:data@theatlantic.com) with one of the following:
1. The URL of a public Github repository that contains your code and instructions.
1. A zip file (or gzipped tarball) containing a git repository with your code and instructions.

## Evaluation Criteria
Your submission will be evaluated primarily on your adherence to the
instructions and on the functional completeness of the solution.

Extra points will be awarded for:
1. A full git history showing your development style.
1. Normalization of the database
1. Authentication and authorization capabilities
1. Support for files larger than 3MB (upload progress indicator, etc)
1. Irregularity detection and alerting (for instance, if a purchase is canceled that has not been previously seen as new)
1. Detecting and handling updating addresses for customers
1. Tests

## Notes
* The goal is to see what you are able to accomplish in an hour or two (max).
  If you're still working after 2 hours, please just document (1) what you
  were able to complete and (2) what you would do if you were to devote more
  time to the challenge - and then submit those descriptions along with
  whatever code you've completed (following the Submission instructions
  above).
* Please submit your solution within a few days of receiving the challenge.
* Please feel free to email [data@theatlantic.com](mailto:data@theatlantic.com) with any questions.
