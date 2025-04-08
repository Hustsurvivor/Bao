import json
import model
import math

def get_training_data(plan_path):
    with open(plan_path)as f:
        plan_lines = f.readlines()[:10]

    plan_list = []
    for line in plan_lines:
        plan_list.extend(line.split('#####')[1:])

    plan_list = [ (json.loads(plan)[0], math.log(1.0 + json.loads(plan)[0]['Execution Time'])) for plan in plan_list]
    return plan_list

def train(model_path, plan_path):

    all_experience = get_training_data(plan_path)
    x = [i[0] for i in all_experience]
    y = [i[1] for i in all_experience]        
    
    reg = model.BaoRegression(have_cache_data=False, verbose=True)
    reg.fit(x, y)
    reg.save(model_path)
    return reg

if __name__  == '__main__':
    train('model/Bao_test', '/app/workload/imdb-former-new/train/template0/plan.txt')