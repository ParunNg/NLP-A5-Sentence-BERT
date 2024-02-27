from flask import Flask, render_template, request
from bert import *
from transformers import BertTokenizer
import torch

app = Flask(__name__)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

params, state = torch.load('../model/s-bert.pt')
model = BERT(**params, device=device).to(device)
model.load_state_dict(state)
# classifier_head = torch.load('../model/classifier-head-custom-bert.pt').to(device)
model.eval()
# classifier_head.eval()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # Hyperparameters for model inference
        sentence_a = request.form['sentence_a']
        sentence_b = request.form['sentence_b']
        score = calculate_similarity(model, tokenizer, params['max_len'], sentence_a, sentence_b, device)

        return render_template('home.html', sentence_a=sentence_a, sentence_b=sentence_b, output=round(score, 4))

    else:
        return render_template('home.html', sentence_a="", sentence_b="", output=None)

if __name__ == '__main__':
    app.run(debug=True)