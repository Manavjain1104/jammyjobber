import { pipeline, AutoModel, AutoTokenizer } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.15.0';

onmessage = async function(e) {
    
    let pipe = await pipeline('text2text-generation', 'Xenova/LaMini-Flan-T5-783M');
    let job_query = e.data[0];
    let job = e.data[1];
    let out = await pipe("Candidate said: " + job_query + job + "Give 4 bulletpoints explaining why the suggested job was a good fit for you or a bad fit.", {
        max_new_tokens: 1000,
    });
    let text = out[0].generated_text

    // Find the index of the 4th dash
    let fourthDashIndex = -1;
    for (let i = 0, count = 0; i < text.length; i++) {
        if (text[i] === '-' && text[i + 1] === ' ') {
            count++;
            if (count === 5) {
                fourthDashIndex = i;
                break;
            }
        }
    }

    // If the 4th dash was found, manipulate the string accordingly
    if (fourthDashIndex !== -1) {
        text = text.substring(0, fourthDashIndex).replaceAll("- ", "<br>- ");
    } else {
        text = text.replaceAll("- ", "<br>- ")
    }
    self.postMessage(text);
};