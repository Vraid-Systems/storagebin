def is_image(content_type):
    """is the given content_type string for an image
    
    Args:
        content_type: string containing Content-Type HTTP header value
    
    Returns:
        Boolean
    """
    return (str(content_type).count("image") > 0)
