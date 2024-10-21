import torch
x = torch.rand(5, 3)
print(x)
print(f"GPU available: {torch.cuda.is_available()}")
