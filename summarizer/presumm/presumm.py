from dataset.dataset import Element
from summarizer.summarizer import Summarizer
from typing import List
import os
import argparse
from time import time as time
from summarizer.presumm.presumm_model.src.others.logging import init_logger, \
    logger
import torch
from pytorch_transformers import BertTokenizer
from summarizer.presumm.presumm_model.src.models import data_loader
from summarizer.presumm.presumm_model.src.models.model_builder import \
    AbsSummarizer
from summarizer.presumm.presumm_model.src.models.predictor import \
    build_predictor


# TODO: Overwrite summarize_dataset to concatenate documents, summarize,
#  and split results. Should be nontrivially more effficient.
# TODO: Clean up temp directory after running.
class PreSummSummarizer(Summarizer):
    """
    Simple summarizer based on PreSumm's BERTExtAbs summarizer. Uses
    abstractive summarization.
    """

    @staticmethod
    def _summarize_file(input_path: str) -> str:
        """
        Summarize the given temp input file in a temp output file and return
        the output file path.
        :param input_path: The input file to summarize.
        :return: The path to the summary file.
        """
        timestamp = str(time())
        # Adapted from `presumm_model/src/train.py`
        # and `presumm_model/src/train_absstractive.py`
        args = argparse.Namespace()

        # TODO: Clean up excess parameters

        # Important
        setattr(args, 'task', 'abs')
        setattr(args, 'encoder', 'bert')
        setattr(args, 'mode', 'test_text')
        setattr(args, 'model_path', 'summarizer/presumm/presumm_model/models/')
        setattr(args, 'result_path', f'summarizer/presumm/temp/{timestamp}')
        setattr(args, 'temp_dir', 'summarizer/presumm/presumm_model/temp')
        setattr(args, 'text_src', f'summarizer/presumm/temp/{input_path}')
        setattr(args, 'test_from', 'summarizer/presumm/presumm_model/models/model_step_148000.pt')
        # Other
        setattr(args, 'bert_data_path', 'summarizer/presumm/presumm_model/bert_data_new/cnndm')
        setattr(args, 'text_tgt', '')
        setattr(args, 'batch_size', 140)
        setattr(args, 'test_batch_size', 200)
        setattr(args, 'max_ndocs_in_batch', 6)
        setattr(args, 'max_pos', 512)
        setattr(args, 'use_interval', True)
        setattr(args, 'large', False)
        setattr(args, 'load_from_extractive', '')
        setattr(args, 'sep_optim', False)
        setattr(args, 'lr_bert', 0.002)
        setattr(args, 'lr_dec', 0.002)
        setattr(args, 'use_bert_emb', False)
        setattr(args, 'share_emb', False)
        setattr(args, 'finetune_bert', True)
        setattr(args, 'dec_dropout', 0.2)
        setattr(args, 'dec_layers', 6)
        setattr(args, 'dec_hidden_size', 768)
        setattr(args, 'dec_heads', 8)
        setattr(args, 'dec_ff_size', 2048)
        setattr(args, 'enc_hidden_size', 512)
        setattr(args, 'enc_ff_size', 512)
        setattr(args, 'enc_dropout', 0.2)
        setattr(args, 'enc_layers', 6)
        setattr(args, 'ext_dropout', 0.2)
        setattr(args, 'ext_layers', 2)
        setattr(args, 'ext_hidden_size', 768)
        setattr(args, 'ext_heads', 8)
        setattr(args, 'ext_ff_size', 2048)
        setattr(args, 'label_smoothing', 0.1)
        setattr(args, 'generator_shard_size', 32)
        setattr(args, 'alpha', 0.6)
        setattr(args, 'beam_size', 5)
        setattr(args, 'min_length', 15)
        setattr(args, 'max_length', 150)
        setattr(args, 'max_tgt_len', 140)
        setattr(args, 'param_init', 0.0)
        setattr(args, 'param_init_glorot', True)
        setattr(args, 'optim', 'adam')
        setattr(args, 'lr', 1)
        setattr(args, 'beta1', 0.9)
        setattr(args, 'beta2', 0.999)
        setattr(args, 'warmup_steps', 8000)
        setattr(args, 'warmup_steps_bert', 8000)
        setattr(args, 'warmup_steps_dec', 8000)
        setattr(args, 'max_grad_norm', 0.0)
        setattr(args, 'accum_count', 1)
        setattr(args, 'report_every', 1)
        setattr(args, 'train_steps', 1000)
        setattr(args, 'recall_eval', False)
        setattr(args, 'visible_gpus', '-1')
        setattr(args, 'gpu_ranks', '0')
        setattr(args, 'log_file', 'summarizer/presumm/presumm_model/logs/cnndm.log')
        setattr(args, 'seed', 666)
        setattr(args, 'test_all', False)
        setattr(args, 'test_start_from', -1)
        setattr(args, 'train_from', '')
        setattr(args, 'report_rouge', True)
        setattr(args, 'block_trigram', True)

        args.gpu_ranks = [int(i) for i in
                          range(len(args.visible_gpus.split(',')))]
        args.world_size = len(args.gpu_ranks)
        os.environ["CUDA_VISIBLE_DEVICES"] = args.visible_gpus

        init_logger(args.log_file)

        logger.info('Loading checkpoint from %s' % args.test_from)
        device = "cpu"

        model_flags = ['hidden_size', 'ff_size', 'heads', 'emb_size',
                       'enc_layers', 'enc_hidden_size', 'enc_ff_size',
                       'dec_layers', 'dec_hidden_size', 'dec_ff_size',
                       'encoder', 'ff_actv', 'use_interval']

        checkpoint = torch.load(args.test_from,
                                map_location=lambda storage, loc: storage)
        opt = vars(checkpoint['opt'])
        for k in opt.keys():
            if (k in model_flags):
                setattr(args, k, opt[k])
        print(args)

        model = AbsSummarizer(args, device, checkpoint)
        model.eval()

        test_iter = data_loader.load_text(args, args.text_src, args.text_tgt,
                                          device)

        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased',
                                                  do_lower_case=True,
                                                  cache_dir=args.temp_dir)
        symbols = {'BOS': tokenizer.vocab['[unused0]'],
                   'EOS': tokenizer.vocab['[unused1]'],
                   'PAD': tokenizer.vocab['[PAD]'],
                   'EOQ': tokenizer.vocab['[unused2]']}
        predictor = build_predictor(args, tokenizer, symbols, model, logger)
        predictor.translate(test_iter, -1)

        return f"{timestamp}.-1.candidate"

    def summarize_element(self, element: Element) -> str:
        """
        Perform abstractive text summarization on an input element.
        WARNING: If possible, do not use this method. Summarizer has best
        efficiency when applied at the document level.
        :param element: An element to summarize.
        :return A summary of the element.
        """
        # Store element in temp file
        timestamp = str(time())
        with open(f'summarizer/presumm/temp/{timestamp}', 'w+') as f:
            f.write(element)
        # Call document summarization helper function on temp file to temp file
        out = self._summarize_file(timestamp)
        # Read summary and return as string
        with open(f'summarizer/presumm/temp/{out}', 'r') as f:
            return f.read()

    def summarize_document(self, document_name: str, fp: str = None) \
            -> List[str]:
        """
        Overwrites the parent class's document summarization method.
        :param document_name: The document to summarize.
        :param fp: The path to the output file. Default None.
        :return: A list of summaries for each element in the dataset.
        """
        # Store document in temp file
        # Call document summarization helper function on temp file to temp file
        # Read summaries and return as list
        # Store document in temp file
        document = self.dataset.retrieve_document(document_name)
        timestamp = str(time())
        with open(f'summarizer/presumm/temp/{timestamp}', 'w+') as f:
            f.write('\n'.join(document))
        # Call document summarization helper function on temp file to temp file
        out = self._summarize_file(timestamp)
        # Read summary and return as string
        with open(f'summarizer/presumm/temp/{out}', 'r') as f:
            summaries = f.readlines()
        if fp is not None:
            self.save(document, summaries, fp)
        return summaries
