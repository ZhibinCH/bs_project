# evaluator.py
# Standard library imports
from datetime import datetime
import time

# Third-party imports
import lmstudio as lms
import pandas as pd

class PostEvaluator:
    def __init__(self):
        self.model = lms.llm("llama-3.2-3b-instruct")
    
    def evaluate_post(self, post):
         
        content = post['content']
        prompt = f"""
        Analyze the following social media post and provide a comprehensive evaluation:
        
        Post: {content}
        
        Your evaluation should include:
        1. Relevance score (1-10): How relevant is this content to our platform/community? (10 = Directly about Solana, 1 = No clear connection)
        2. Risk level (low/medium/high): Does this post contain any risky content? (high = Scams, misinformation, hate speech)
        3. Reliability score (1-10): How reliable is the information in this post? (10 = Verified source + citations, 1 = Demonstrably false)
        4. Sentiment (positive/neutral/negative): What's the overall sentiment?
        5. Credibility (1-10): How credible is the source/content? (10 = Verified source, 1 = Anonymous account or past misinformation)
        6. Category tags (comma-separated): What categories does this post belong to?
        
        Please format your response as:
        Relevance: [score]
        Risk: [level]
        Reliability: [score]
        Sentiment: [sentiment]
        Credibility: [score]
        Categories: [tags]
        """
        
        try:
            response = self.model.respond(prompt)
            evaluation = self._parse_response(response)
            return {
                **evaluation,
                'evaluation_raw': str(response),
                'evaluated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"Evaluation error: {e}")
            return self._default_evaluation()

    def _parse_response(self, response):
        """Parse LLM response into structured dict"""
        evaluation = {}
        for line in str(response).split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                evaluation[key.strip().lower()] = value.strip()
        return {
            'relevance_score': int(evaluation.get('relevance', 5)),
            'risk_level': evaluation.get('risk', 'medium'),
            'reliability_score': int(evaluation.get('reliability', 5)),
            'sentiment': evaluation.get('sentiment', 'neutral'),
            'credibility': int(evaluation.get('credibility', 5)),
            'categories': evaluation.get('categories', 'uncategorized')
        }

    def _default_evaluation(self):
        """Return default values when evaluation fails"""
        return {
            'relevance_score': 5,
            'risk_level': 'medium',
            'reliability_score': 5,
            'sentiment': 'neutral',
            'credibility': 5,
            'categories': 'uncategorized',
            'evaluation_raw': 'Error in evaluation'
        }

def evaluate_dataframe(df):
    
    evaluator = PostEvaluator()
    evaluations = []
    
    print(f"Evaluating {len(df)} posts...")
    for _, row in df.iterrows():
        evaluations.append(evaluator.evaluate_post(row))
        time.sleep(1)  # Rate limiting
    
    return pd.concat([df, pd.DataFrame(evaluations)], axis=1)

if __name__ == "__main__":
    
    # For standalone testing
    # test_df = pd.read_csv("solana_tweets_20250330.csv")
    # print(evaluate_dataframe(test_df))
    test_post = {
        'content': 'Solana just announced a major upgrade!',
        'username': 'SolanaOfficial',
        'timestamp': datetime.now().isoformat()
    }
    print(PostEvaluator().evaluate_post(test_post))