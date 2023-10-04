from langchain.llms import GPT4All

llm = GPT4All(
    model="models/orca-mini-3b.ggmlv3.q4_0.bin",  # orca-mini - 13.5sec, falcon - 17sec, ggml-mini - 3.5sec(no result)
    max_tokens=2048,
)


# print(llm("You are a hospital assistant conversing with various patients and help them in a hospital."))

# import pdb
# pdb.set_trace()

print(llm("I have pain in my bone please suggest me which doctor should I refer to ?"))