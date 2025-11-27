from mcp.server.fastmcp import FastMCP

mcp = FastMCP("promptandresource-mcp-demo")

@mcp.resource("docs://aboutme")
def partha_bio() -> str:
    return (
        """
        Partha Biswas is a software professional with over 12 years of experience in Java 
        programming and cloud-native development. He is a VP Engineering [Platform Engineering] at 
        JPMorgan&Chase , where he designs and implements scalable, resilient, and efficient software 
        solutions on cloud platforms which are used across different Lines-of-businesses . 
        He is also an Oracle Certified Java Professional and have hands-on experience with a diverse 
        range of technologies,  which includes :
        
        Java,Spring,SpringBoot,SpringSecurity, Concurrency & Multithreading, 
        Messaging Frameworks like ActiveMQ, RabbitMQ, Kafka,
        Communication protocols: REST, SOAP, gRPC, GraphQL
        Caching (EhCache, Redis),
        RDBMS (like mysql, oracle, microsoft sql-server, postgres) ,
        NoSQL databases (mongodb and elasticsearch), 
        cloud platforms such as AWS, Azure
        containerization tools like Docker and Kubernetes,
        and microservices architecture.
        
        He specialize in creating robust and scalable applications using cutting-edge frameworks and tools, 
        following the best practices of cloud-native development. I have successfully delivered complex 
        projects, collaborating with cross-functional teams to meet business objectives and exceed client 
        expectations. Partha is a proactive problem-solver, who continuously stays updated on emerging trends 
        and technologies in the cloud-native landscape. He is also passionate about innovation and leveraging
        the latest tools and methodologies to deliver high-quality, scalable solutions.
        
        If you are looking for a skilled and experienced Java cloud-native TechLead / Consultant / Architect,
        then he would be the best person discuss potential opportunities. 
        """
    )
@mcp.prompt("question")
def ask_about_partha(question:str, context:str) -> str:
    return (
        "System: you are a helpful assistant. Answer strictly using the provided context."
        f"Context:{context}"
        f"User Question : {question}"
        "Answer:"
    )

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

