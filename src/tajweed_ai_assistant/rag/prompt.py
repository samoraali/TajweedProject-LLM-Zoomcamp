from __future__ import annotations


SYSTEM_PROMPT = """
أنت مساعد ذكي متخصص في أحكام التجويد.

مهمتك الإجابة عن أسئلة المستخدم بالاعتماد على سياق ملزمة التجويد
المقدم لك فقط.

قواعد الإجابة:
1. أجب باللغة العربية.
2. استخدم المعلومات الموجودة في السياق فقط.
3. لا تضف معلومة من معرفتك العامة إذا لم يذكرها السياق.
4. لا تستنتج حكمًا أو تفصيلًا غير مدعوم بوضوح من السياق.
5. إذا كان السياق لا يحتوي على معلومات كافية للإجابة، قل بوضوح:
   "لا أجد في السياق المسترجع معلومات كافية للإجابة عن هذا السؤال."
6. إذا كانت المعلومات متوفرة، قدم إجابة واضحة ومختصرة ومناسبة لطالب يتعلم التجويد.
7. لا تنسب معلومة إلى الملزمة إذا لم تكن موجودة في السياق.
8. عند استخدام معلومة من مصدر، اذكر رقم الصفحة إذا كان متاحًا في السياق.
9. إذا كان السؤال خارج موضوع التجويد أو خارج المعلومات الموجودة في السياق،
   وضّح أن السياق الحالي لا يكفي للإجابة بدلًا من التخمين.
"""


def build_context(results: list[dict]) -> str:
    """Build the context section from retrieved knowledge-base chunks."""
    context_parts = []

    for i, result in enumerate(results, start=1):
        page = result.get("pdf_page", result.get("page", "غير معروف"))
        topic = result.get("topic", "غير معروف")
        text = result.get("text", "").strip()

        context_parts.append(
            f"""المصدر {i}
الصفحة: {page}
الموضوع: {topic}

{text}
"""
        )

    return "\n---\n".join(context_parts)


def build_rag_prompt(
    query: str,
    results: list[dict],
) -> str:
    """Build the user prompt containing the question and retrieved context."""
    context = build_context(results)

    return f"""
السؤال:
{query}

السياق المسترجع من ملزمة التجويد:
{context}

أجب عن السؤال اعتمادًا على السياق أعلاه فقط.
"""
