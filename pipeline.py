from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

def run_research_pipline(topic:str) -> dict :

    state = {}

    # step 1 - search agent working
    print("\n"+" ="*50)
    print("Step 1 - Search agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    searched_result = search_agent.invoke({
        "messages":[("user", f"Find recent, reliable and detailed information about : {topic}")]
    })
    state["search_results"] = searched_result["messages"][-1].content

    print("\n search result ", state['search_results'])

    # step 2 - reader agent
    print("\n"+" ="*50)
    print("Step 2 - Reader agent is scraping top resources ...")
    print("="*50)

    reaader_agent = build_reader_agent()
    reader_result = reaader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}',"
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })
    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nScraped content\n", state['scraped_content'])

    #step 3 - writer Chain
    print("\n"+" ="*50)
    print("Step 3 - Writer is drafting the report ...")
    print("="*50)

    research_combined = (
    f"SEARCH RESULTS:\n{state['search_results']}\n\n"
    f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic":topic,
        "research":research_combined
    })

    print("\n Final Report\n : ", state['report'])

    # step 4 - critic report
    print("\n"+" ="*50)
    print("Step 4 - Critic is reviewing the report ...")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })

    print("\nCritic Report\n : ", state['feedback'])

    return state

if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipline(topic)

