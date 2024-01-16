import openai
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1", # "http://<Your api-server IP>:port"
    api_key = "sk-no-key-required"
)

def generate_summary(job_description):
    """Generates a summary from a job description using LLaMafile via the local API server."""

    messages = [
        {"role": "system", "content": "Summarize the following job description:"},
        {"role": "user", "content": job_description},
    ]

    # Call the local API server to generate the summary
    response = client.chat.completions.create(model="LLaMA_CPP",
    messages=messages,
    max_tokens=1000,  # Adjust max_tokens as needed
    n=1,
    stop=None,
    temperature=0.0)

    summary = response.choices[0].message.content.strip()

    # Prepare the summary for embedding in a vector database (details omitted for brevity)

    return summary

# Example usage:
job_description = """
We are tooth - an exceptional, award winning fully private surgery in the heart of Waterloo SE1 with two branches (general and specialist). We are looking for a new full time Dental Receptionist to join our amazing team.

We have won and been recognised at multiple awards, including Best Dental Practice in London and we have hundreds of 5 star reviews on Google. The real secret of our success is our team!

Our team is important to us – we only employ people with the right skills, the right drive and the right attitude – people that care as much as we do about doing the best for our customers.

The role:

Receptionist (35hrs-40hrs average per week - made up of 6-8hrs per day Mon to Friday PLUS at least one in every three Saturdays (more Saturdays may be available if wanted).

Salary: Very competitive Salary for great candidates

Hours: On Mondays to Fridays you will be needed every day from either 8.00am - 2.00pm or 2.00pm to 8.00pm - this will be on rota with the other receptionists. On some days you may be needed from 9.00am to 6.00pm. On Saturdays (at least one in three) the hours are 10.00am - 4.00pm.

If you cannot do the above shifts from Monday to Friday please do not apply. There is no flexibility in the timings of the shifts.

You will be the face of our business, so you must be very presentable, friendly and approachable and offer exceptional customer service - face to face, on the phone and on emails. It is therefore essential that you have fluent English language skills - written and spoken, and that you are a confident and friendly communicator and great on the phone.

Full training will be given, dental reception experience required. You will need to enjoy learning new things, be quick to learn, intelligent with good initiative and confidence.

This is a super exciting reception role in a busy practice - not a basic name badge giving or 'checking in' reception role - you will need to be smart and open to learning things and want to grow with us as a business, and confident with dealing with calls and multi-tasking.

Ideal candidates must possess:

- Relevant UK dental reception experience

- Excellent English language skills – both written and spoken

- Strong IT skills

- Organised, ability to multi-task and calm under pressure

- A can do attitude with excellent personal presentation

**Dental reception experience is required for this role**

We offer a great working environment where you will always be treated well, respected and valued as part of a very friendly team. Full training will be given. To find out more about us, our brand and what we are all about please visit our website at www.toothlondon .co.uk

Apply with your CV and a quick covering letter/email telling us why you think you have what it takes to be part of the tooth team.

We will be able to do out of hours interviews if required. We will not be able to respond to all applicants owing to the numbers of candidates who apply via this website. We are not able to sponsor candidates for this role - you must be in the UK with UK work experience and relevant NI/Visa/Settlement Status as applicable.

Full training will be given before start date. Start date 5th Feb or earlier.

Job Types: Full-time, Permanent

Salary: £30,160.00-£32,240.00 per year

Benefits:

Company pension
Employee discount
Sick pay
Education:

A-Level or equivalent (preferred)
Experience:

Dental receptionist: 1 year (preferred)
Work Location: In person

Application deadline: 19/01/2024
Reference ID: RCPT0124
Expected start date: 05/02/2024
"""
summary = generate_summary(job_description)
print(summary)