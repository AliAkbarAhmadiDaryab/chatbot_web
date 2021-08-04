import pickle as pkl
import os
from chat_bot_package.database_tables import TestDialogueResponse, TestModelPrediction
from chat_bot_package import db


def set_prediction_dialogue():
    global responses, dialogues, res, dia
    model_names = os.walk('./model_outputs/')
    predictions = pkl.load(open(f'./model_outputs/bahdanau_attention_seq2seq_lstm/predictions.pkl', 'rb'))
    responses = pkl.load(open(f'./model_outputs/bahdanau_attention_seq2seq_lstm/responses.pkl', 'rb'))
    dialogues = pkl.load(open(f'./model_outputs/bahdanau_attention_seq2seq_lstm/dialogues.pkl', 'rb'))
    predictions_dict = {'bahdanau_attention_seq2seq_lstm': predictions}
    for i, model_name in enumerate(model_names):
        if i < 2:
            continue
        else:
            res = pkl.load(open(f'{model_name[0]}/responses.pkl', 'rb'))
            dia = pkl.load(open(f'{model_name[0]}/dialogues.pkl', 'rb'))
            pred = pkl.load(open(f'{model_name[0]}/predictions.pkl', 'rb'))
            pred_new = []
            for ri, rs in enumerate(responses):
                for j, re in enumerate(res):
                    if rs == re:
                        if dialogues[ri] == dia[j]:
                            pred_new.append(pred[j])
                            break
            predictions_dict[model_name[0].split('/')[-1]] = pred_new
    pkl.dump(predictions_dict, open(f'./model_outputs/models_predictions.pkl', 'wb'))


def insert_db_dialogue_response():
    responses = pkl.load(open(f'./model_outputs/bahdanau_attention_seq2seq_lstm/responses.pkl', 'rb'))
    dialogues = pkl.load(open(f'./model_outputs/bahdanau_attention_seq2seq_lstm/dialogues.pkl', 'rb'))

    for dia, res in zip(dialogues, responses):
        tdr = TestDialogueResponse(dialogue=dia, response=res)
        db.session.add(tdr)
        db.session.commit()


def insert_db_prediction(dia_id, model_name, prediction):
    pred = TestModelPrediction(id_d_r=dia_id, model_name=model_name, prediction=prediction)
    db.session.add(pred)
    db.session.commit()


if __name__ == '__main__':
    # set_prediction_dialogue()
    # insert_db_dialogue_response()

    pred_to_db = pkl.load(open(f'./model_outputs/models_predictions.pkl', 'rb'))
    model_names = pred_to_db.keys()
    for model_name in model_names:
        for i, pred in enumerate(pred_to_db[model_name]):
            insert_db_prediction(i+1, model_name=model_name, prediction=pred)
    print(pred_to_db)
