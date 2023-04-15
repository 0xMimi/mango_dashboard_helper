V4_TOKEN_DEPOSIT = """
SELECT 
  date_trunc('day',block_timestamp) AS date,
  tx_id,
  account_keys,
  pre_balances,
  post_balances,
  pre_token_balances,
  post_token_balances
FROM 
  solana.core.fact_transactions, 
  LATERAL FLATTEN(log_messages) AS log,
  LATERAL FLATTEN(instructions) AS instruction
WHERE 
  log.value = 'Program log: Instruction: TokenDeposit'
AND 
  instruction.value:programId = '4MangoMjqJ2firMokCjjGgoK8d4MXcrgL7XJaL3w6fVg'
AND 
  succeeded = TRUE
AND 
  date >= '2023-03-05'
ORDER BY date ASC;
"""

TOKEN_PRICES = """
SELECT
  date_trunc('day', recorded_hour) AS date,
  token_address AS mint,
  AVG(close) AS price
FROM
  solana.core.ez_token_prices_hourly
WHERE
  token_address IN (
    '7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs',
    'MangoCzJ36AjZyKwVj3VnYU4GTonjfVEnJmvvWaxLac',
    'mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So',
    'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
    'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB',
    '3NZ9JMVBmGAqocybic2c7LQCJScmgsAZ6vQqTDzcqmJh',
    'So11111111111111111111111111111111111111112',
    'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263'
  )
  AND date >= '2023-03-05'
GROUP BY
  date,
  mint
ORDER BY
  date;
"""
