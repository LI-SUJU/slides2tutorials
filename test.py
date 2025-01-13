import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add nodes for the process
nodes = [
    "Upload Lecture Slides (PDF)",
    "Customize Options",
    "Extract Text from PDF",
    "Clean and Preprocess Text",
    "Summarize Content",
    "Generate Narrative (User Preferences)",
    "Combine Narratives into Audio",
    "Generate PDF with Narratives",
    "Provide Download Links",
    "Clear Temporary Files"
]

# Add edges for the flow
edges = [
    ("Upload Lecture Slides (PDF)", "Customize Options"),
    ("Customize Options", "Extract Text from PDF"),
    ("Extract Text from PDF", "Clean and Preprocess Text"),
    ("Clean and Preprocess Text", "Summarize Content"),
    ("Summarize Content", "Generate Narrative (User Preferences)"),
    ("Generate Narrative (User Preferences)", "Combine Narratives into Audio"),
    ("Generate Narrative (User Preferences)", "Generate PDF with Narratives"),
    ("Combine Narratives into Audio", "Provide Download Links"),
    ("Generate PDF with Narratives", "Provide Download Links"),
    ("Provide Download Links", "Clear Temporary Files")
]

# Add nodes and edges to the graph
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# Draw the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)  # Layout for the nodes
nx.draw(
    G, pos, with_labels=True, node_color="skyblue", node_size=3000, font_size=10,
    font_weight="bold", arrowsize=20, edge_color="gray"
)

plt.title("Flow Diagram of Lecture Slide to Tutorial Generator Interface", fontsize=14)
plt.savefig("flow_diagram.png")
