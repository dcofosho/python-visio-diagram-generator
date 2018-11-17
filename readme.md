<h1>Python Visio Diagram Generator</h1>

<p>
This is some code for drawing a basic Visio diagram illustrating a set of hierarchically nested objects using Python. Currently it can only draw a hierarchy 3 levels deep, with a single root object, all centered around a single horizontal line. I plan to update this code to support deeper trees drawn in a more versatile and aesthetically pleasing manner.
</p>

<p>
The code takes a python dictionary representing a tree of hierarchically nested objects (see capability_map.py), which looks like this:
<code>
	capability_map = {
	'Customer Travel Experience' : ['Pre- and Post - Travel Experience', 'Check-In Desks Management', 'Gate Departure Management','Customer Airport Services'],
	'Pre- and Post - Travel Experience': ['Customer Products and Marketing', 'Sales', 'Customer Pre-Travel Experience', 'Access and Transportation', 'Customer Relations', 'Customer Loyalty Management'],
	'Check-In Desks Management': ['Luggage Acceptance', 'Passenger Information Management'],
	'Gate Departure Management': ['Outbound Flight Planning', 'Data Control Management', 'Passenger Boarding Management', 'Flight Closeout and Post Departure Management'],
	'Customer Airport Services': ['Retail Management', 'Lounge Services Management', 'Customer Special Needs Services Management'],
	'Customer Products and Marketing': [], 
	'Sales': [], 
	...
	}
</code>

...And turn it into a Visio diagram which looks like this:

!["output"](https://github.com/dcofosho/python-visio-diagram-generator/blob/master/output.png)

<p>
There is also an example provided for you to test out the code. Thanks to [Orbus Software](https://www.orbussoftware.com/resources/starter-packs/togaf-92-starter-pack/) (where I work) for the stencil. 
</p>

<p>
I'm sharing this on Github for a few reasons:
<ol>
	<li>It might actually be useful to someone out there as is :)</li>
	<li>There is a real lack of existing examples and documentation online regarding how to write python code which manipulates Visio. That's a shame, because it seems that Python can be quite powerful for this use case. I encourage any other Python + Visio users out there to get inspired and make your own projects and share them with me. It would be great to create a toolbox of some open source Python projects for doing cool Visio stuff. Anyone interested in contributing towards this effort contact me at dlcohen@gmail.com!</li>
	<li>The code as is works pretty nicely as is, but is still a tad buggy (run the example to see what I mean). If anyone has any ideas how to improve it, I'd love to hear!</li>
</ol>
</p>

<ul>
<br>
Prerequisites
	<li>This code only runs on Windows machines.</li>
	<li>You will need a command line terminal from which to run the program. I recommend [Git Bash.](https://gitforwindows.org/)</li>
	<li>You will need [Visio](https://support.office.com/en-us/article/install-visio-f98f21e3-aa02-4827-9167-ddab5b025710). I recommend Visio Pro 2016.</li>
	<li>[Download Python 3](https://www.python.org/downloads/). If you're not sure if you have it already, you can check by running <code>python -v</code> from your command line terminal.</li>
</ul>

<ul>
How to run
	<li>Download or clone the repository to your local machine.</li>
	<li>In your command line terminal, navigate to the project folder using cd.</li>
	<li>Enter the command <code>python diagram_generator.py</code> to run the code on the provided example data.</li>
	<li>To use this code for a custom project, edit capability_map.py to reflect your data set, and the arguements in diagram_generator.py to reflect the paths of the stencil and template on your machine as well as the desired output path.</li>
</ul>

