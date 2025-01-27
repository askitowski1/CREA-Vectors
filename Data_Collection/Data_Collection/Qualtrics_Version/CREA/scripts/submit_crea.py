# Code to submit a CREA job using the MTurk API
#
# Bill Gross, 7/27/23

import boto3
import re,base64,json

test_mode = False

if test_mode:
    MTURK_URL = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
    MTURK_SUBMIT = 'https://workersandbox.mturk.com/mturk/externalSubmit'
else:
    MTURK_URL = 'https://mturk-requester.us-east-1.amazonaws.com'
    MTURK_SUBMIT = 'https://www.mturk.com/mturk/externalSubmit'

survey_baseurl = 'https://mcwisc.co1.qualtrics.com/jfe/form/SV_5dt5OUxI4gjbNb0?Q_EED='

def create_surveylink(word,sentence):
    enc_string = '{"word":"%s","example":"%s"}' % (word,sentence)
    args = base64.urlsafe_b64encode(bytes(enc_string,'utf-8')).decode('utf-8')
    url = f'{survey_baseurl}{args}'
    return url


mturk = boto3.client('mturk',endpoint_url = MTURK_URL)

def create_question(word,sentence):
    url = create_surveylink(word,sentence)

    return f'''
<HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
  <HTMLContent><![CDATA[
<!DOCTYPE html>
<html>
<!-- For help on using this template, see the blog post: https://blog.mturk.com/editing-the-survey-link-project-template-in-the-ui-7c75285105fb#.py7towsdx --><!-- HIT template: SurveyLink-v3.0 --><!-- The following snippet enables the 'responsive' behavior on smaller screens -->
<meta content="width=device-width,initial-scale=1" name="viewport" />
<section class="container" id="SurveyLink"><!-- Instructions -->
<div class="row">
<div class="col-xs-12 col-md-12">
<div class="panel panel-primary"><!-- WARNING: the ids "collapseTrigger" and "instructionBody" are being used to enable expand/collapse feature --><a class="panel-heading" href="javascript:void(0);" id="collapseTrigger"><strong>Survey Link Instructions</strong></a>
<div class="panel-body">
<h3>If English is your first language: Take a survey about the meaning of a word</h3>

<p>The Medical College of Wisconsin is conducting a survey about the meaning of words in English. Select the link below to complete the survey about one of the words. It should take around 15 minutes to complete it, but you will have up to 1 hour. At the end of the survey, you will receive a code to paste into the box below to receive credit for your work. Please make sure to answer all the questions and record your code before leaving the survey page.</p>

<p>There are several versions of this HIT, you are encouraged to complete it as many times as you wish. Each time you will be given a different word to rate.</p>

<p class="well well-sm"><strong><mark>ATTENTION:</mark></strong> - The HIT will only be approved if responses indicate compliance with the instructions. Randomly provided responses will be rejected and the Worker will be blocked from future HITs. It may take up to 7 days after completion for HITs to be reviewed and accepted.</p>

<p>It may take up to 7 days after completion for HITs to be reviewed and accepted.</p>

<p />

<p><strong>Principal Investigator:</strong><br />
Jeffrey Binder, MD<br />
Professor of Neurology, Medical College of Wisconsin<br />
jbinder@mcw.edu</p>

</div>
</div>
</div>
</div>
<!-- End Instructions --><!-- Survey Link Layout -->


<form name="mturk_form" method="post" id="mturk_form" action="{MTURK_SUBMIT}">
<input type="hidden" value="" name="assignmentId" id="assignmentId"/>

<div class="row" id="workContent">
<div class="col-xs-12 col-md-6 col-md-offset-3"><!-- Content for Worker -->

<table class="table table-condensed table-bordered">
	<colgroup>
		<col class="col-xs-4 col-md-4" />
		<col class="col-xs-8 col-md-8" />
	</colgroup>
	<tbody>
		<tr>
			<td><label>Survey link:</label></td>
			<td><a class="dont-break-out" href="{url}" target="_blank">{url}</a></td>
		</tr>
	</tbody>
</table>

<!-- End Content for Worker --><!-- Input from Worker -->

<div class="form-group"><label for="surveycode">Provide the survey code here:</label> <input class="form-control" id="surveycode" name="surveycode" placeholder="e.g. 123456" required="" type="text" /></div>
<!-- End input from Worker --></div>
</div>

<p class="text-center">
    <button onclick="handleFormSubmit()" class="btn btn-primary" id="submitButton">Submit</button>
</p>
</form>

<!-- End Survey Link Layout --></section>
<!-- Please note that Bootstrap CSS/JS and JQuery are 3rd party libraries that may update their url/code at any time. Amazon Mechanical Turk (MTurk) is including these libraries as a default option for you, but is not responsible for any changes to the external libraries --><!-- External CSS references -->
<link crossorigin="anonymous" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css" integrity="sha384-IS73LIqjtYesmURkDE9MXKbXqYA8rvKEp/ghicjem7Vc3mGRdQRptJSz60tvrB6+" rel="stylesheet" /><!-- Open internal style sheet -->
<style type="text/css">#collapseTrigger{{
  color:#fff;
  display: block;
  text-decoration: none;
}}
#submitButton{{
  white-space: normal;
}}
.image{{
  margin-bottom: 15px; 
}}
/* CSS for breaking long words/urls */
.dont-break-out {{
  overflow-wrap: break-word;
  word-wrap: break-word;
  -ms-word-break: break-all;
  word-break: break-all;
  word-break: break-word;
  -ms-hyphens: auto;
  -moz-hyphens: auto;
  -webkit-hyphens: auto;
  hyphens: auto;
}}
</style>
<script>
function handleFormSubmit() {{
  const urlParams = new URLSearchParams(window.location.search)
  document.getElementById('assignmentId').value = urlParams.get('assignmentId')
  document.getElementById('mturk_form').submit()
}}
</script>
</html>
]]>
  </HTMLContent>
  <FrameHeight>0</FrameHeight>
</HTMLQuestion>'''


qr = [
    # Only in US
    {
        'QualificationTypeId': '00000000000000000071',
        'Comparator': 'In',
        'LocaleValues': [{'Country': 'US'}]
    },
    # Number of HITs approved >= 10,000
    {
        'QualificationTypeId': '00000000000000000040',
        'Comparator': 'GreaterThanOrEqualTo',
        'IntegerValues': [10000]
    },
    # HIT Approval Rate >= 99
    {
        'QualificationTypeId': '000000000000000000L0',
        'Comparator': 'GreaterThanOrEqualTo',
        'IntegerValues': [99]
    }
]

# Add the qualification that this worker hasn't previously done this word
def qr_word(word):
   qrw = qr.copy()
   qualid = create_done_qualification(word)
   qrw.append({
      'QualificationTypeId': qualid,
      'Comparator': 'DoesNotExist'
   })
   return qrw

def create_hit(word,sentence,num_assignments):
    response = mturk.create_hit(
        Title = 'The Word Meaning Project',
        Description = 'In this survey you will be given a word and answer a series of questions about its meaning.',
        Keywords = 'word meaning, language, semantics, rating',
        Reward = '1.40',
        MaxAssignments = num_assignments,
        LifetimeInSeconds = 172800,
        AssignmentDurationInSeconds = 432000,
        AutoApprovalDelayInSeconds = 604800,
        Question = create_question(word,sentence),
        QualificationRequirements = qr_word(word)
    )

    hit_group_id = response['HIT']['HITGroupId']
    hit_id = response['HIT']['HITId']
    print("Your HIT has been created.") 
    if test_mode:
      print("You can preview it at this link:")
      print(f"https://workersandbox.mturk.com/mturk/preview?groupId={hit_group_id}")
    print(f"Your HIT ID is: {hit_id}")

def all_hits():
    hits = []
    h = mturk.list_hits()
    while h['NumResults']>0:
      hits.extend([hh['HITId'] for hh in h['HITs']])
      h = mturk.list_hits(NextToken=h['NextToken'])
    return hits

def all_assignments(hitid):
    assignments = []
    a = mturk.list_assignments_for_hit(HITId=hitid)
    while a['NumResults']>0:
      assignments.extend([aa['AssignmentId'] for aa in a['Assignments']])
      a = mturk.list_assignments_for_hit(HITId=hitid,NextToken=a['NextToken'])
    return assignments
    
def get_worker_word(assignmentid):
    a = mturk.get_assignment(AssignmentId=assignmentid)
    question = a['HIT']['Question']
    m = re.search('href="https://mcwisc.co1.qualtrics.co[^"]*\?Q_EED=([^"]*)"',question)
    if m:
      d = base64.urlsafe_b64decode(m[1])
      word = json.loads(d)['word']
      workerid = a['Assignment']['WorkerId']
      return {'word':word,'workerid':workerid}
    else:
      return {'word':None,'workerid':None}

def get_workersforword(word):
    workers = []
    for hit in all_hits():
        for assignment in all_assignments(hit):
            w = get_worker_word(assignment)
            if w['word']==word:
                workers.append(w['workerid'])
    return workers

def create_done_qualification(word):
    name = f'CREA_alreadydone_{word}'
    description = f'Workers that have already complete the CREA word {word}'
    quals = mturk.list_qualification_types(Query=name,MustBeRequestable=True,MustBeOwnedByCaller=True)
    if quals['NumResults']>0:
       qualid = quals['QualificationTypes'][0]['QualificationTypeId']
    else:
       qual = mturk.create_qualification_type(Name=name,Description=description,QualificationTypeStatus='Active')
       qualid = qual['QualificationType']['QualificationTypeId']
    for worker in get_workersforword(word):
       mturk.associate_qualification_with_worker(QualificationTypeId=qualid,WorkerId=worker,IntegerValue=100,SendNotification=False)
    return qualid