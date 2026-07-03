"""
AI Insight Generator
"""


def ai_insights(

    dashboard,

    reliability,

    confidence_dashboard

):

    insights = []

    if dashboard["positive_percentage"] > 70:

        insights.append(

            "Most reviews are positive."

        )

    elif dashboard["negative_percentage"] > 70:

        insights.append(

            "Most reviews are negative."

        )

    else:

        insights.append(

            "User opinions are mixed."

        )

    if reliability["risk"] == "Very Low":

        insights.append(

            "Prediction reliability is excellent."

        )

    elif reliability["risk"] == "Low":

        insights.append(

            "Prediction reliability is high."

        )

    else:

        insights.append(

            "Prediction should be interpreted carefully."

        )

    if confidence_dashboard["average"] > 90:

        insights.append(

            "Models are highly confident."

        )

    elif confidence_dashboard["average"] > 75:

        insights.append(

            "Models show good confidence."

        )

    else:

        insights.append(

            "Model confidence is relatively low."

        )

    return insights