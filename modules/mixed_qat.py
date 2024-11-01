
from .apply_qat import apply_QAT
from torch import nn

class MixedQATBERT(nn.Module):
    def __init__(self, model, attention_bits=8, ffn_bits=4):
        super(MixedQATBERT, self).__init__()
        self.bert = model
        # 각 레이어마다 attention과 FFN에 다른 quantization 적용
        for layer in self.bert.bert.encoder.layer:
            layer.attention.self = apply_QAT(layer.attention.self, precision = attention_bits, mode = 'attention')

            layer.intermediate.dense = apply_QAT(layer.intermediate.dense, precision = 4, mode = 'ffn')
            layer.output.dense = apply_QAT(layer.output.dense, precision = ffn_bits, mode = 'ffn')

    # def forward(self, input_ids, attention_mask=None):
    #     return self.bert(input_ids, attention_mask)
    def forward(self, input_ids, attention_mask=None, token_type_ids=None, labels=None):
        # BertForSequenceClassification의 forward에 모든 인수를 전달
        return self.bert(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids, labels=labels)
