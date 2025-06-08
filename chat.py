import openai
import razorpay
# Razorpay setup: Replace with your Razorpay API keys
razorpay_client = razorpay.Client(auth=("rzp_test_XCq4jOQB1ymjhj", "AiiiVxIPAkYuRYIiGEveDYGu"))

# OpenAI API setup
openai.api_key = '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'
bot_name = "Hinata"

def get_response(msg):
    try:
        # If the message indicates a payment request, handle it separately
        if "payment" in msg.lower() or "pay" in msg.lower():
            amount = 50000  # Example amount in paise (₹500.00)
            payment_order = create_payment_order(amount)
            return f"Please complete the payment using this link: {payment_order}"

       # Use the newer GPT-3.5-turbo model or GPT-4 instead of text-davinci-003
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can also use 'gpt-4' if available and necessary
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},  # System message
                {"role": "user", "content": msg}  # User message
            ],
            max_tokens=150,  # Adjust max_tokens as needed
            temperature=0.7  # Adjust temperature for creativity vs. accuracy
        )
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"Error: {str(e)}"

def create_payment_order(amount):
    """
    This function creates a Razorpay payment order and returns the payment URL.
    :param amount: The amount to be charged (in paise).
    :return: Payment URL
    """
    try:
        # Create a Razorpay order
        order = razorpay_client.order.create({
            "amount": amount,  # Amount in paise (₹500.00 = 50000 paise)
            "currency": "INR",
            "payment_capture": 1  # Auto capture the payment after authorization
        })

        # Generate a payment link (you would typically integrate this with your frontend)
        payment_url = f"https://checkout.razorpay.com/v1/checkout.js?order_id={order['id']}"
        return payment_url

    except Exception as e:
        return f"Error in creating payment order: {str(e)}"

# Example usage for testing
if _name_ == "_main_":
    user_input = "I would like to make a payment"
    print("User:", user_input)
    print("Bot:", get_response(user_input))