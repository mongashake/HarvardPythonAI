import os
import random
import re
import sys
from collections import Counter
from math import isclose

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = {}

    links_on_page: set = corpus.get(page, set())

    ## if no links on page, randomize from all pages in corpus
    if not links_on_page:
        distribution = {each_page: 1/len(corpus) for each_page in corpus.keys()}
        assert sum(distribution.values()) == 1.0
        return distribution

    ## remove link to itself
    if page in links_on_page:
        links_on_page.remove(page)

    distribution = {each_page: damping_factor/len(links_on_page) for each_page in links_on_page}
    for each_page in corpus.keys():
        if each_page in distribution:
            distribution[each_page] += (1 - damping_factor)/len(corpus)
        else:
            distribution[each_page] = (1 - damping_factor)/len(corpus)

    assert isclose(sum(distribution.values()), 1.0)
    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pagerank = []
    start = random.choice(list(corpus.keys()))
    pagerank.append(start)
    transition = transition_model(corpus, start, damping_factor)
    samples = n
    samples -= 1

    while samples > 0:
        cumulative_transition = {}
        jump = 0

        ## create cumulative distribution
        for each_page, probability in transition.items():
            jump += probability
            cumulative_transition[each_page] = jump
    
        choose = random.random()
        for each_page, probability in cumulative_transition.items():
            if choose <= probability:
                pagerank.append(each_page)
                transition = transition_model(corpus, each_page, damping_factor)
                break

        samples -= 1

    pagerank = Counter(pagerank)
    pagerank = {k: v/n for k,v in pagerank.items()}
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    accuracy = 0.001
    def numlinks(page):
        return len(corpus.get(page))

    def pr(page):
        ## primary pagerank algorithm

        rank = (1 - damping_factor) / len(inverse_corpus) +\
        damping_factor * sum([pagerank.get(curr_page) / numlinks(curr_page)\
                            for curr_page in inverse_corpus.get(page, set())])
        return rank

    ## inverse_corpus -> key: page, value: set of all pages that link to key
    inverse_corpus = {curr_page: set() for curr_page in corpus.keys()}
    for curr_page, links in corpus.items():
        if not links:
            links = set(corpus.keys())
            corpus[curr_page] = links

        for link in links:
            inverse_corpus[link].add(curr_page)

    pagerank = {curr_page: 1/len(corpus) for curr_page in corpus.keys()}
    diff = []
    while True:
        for curr_page, curr_rank in pagerank.items():
            updated_pr = pr(curr_page)
            diff.append(isclose(curr_rank, updated_pr, rel_tol=accuracy))
            pagerank[curr_page] = updated_pr

        if all(diff) and isclose(sum(pagerank.values()), 1.0):
            break
        diff = []

    return pagerank

if __name__ == "__main__":
    main()
