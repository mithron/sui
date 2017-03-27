import pystan
model_code = """
data {
  int n;                                
  int m;                                
  matrix[n, m] A;
  vector[n] y;
}

parameters {
  vector[m] delta;
}

model {y ~ normal(A * delta,1);}
"""
model = pystan.StanModel(model_code=model_code)