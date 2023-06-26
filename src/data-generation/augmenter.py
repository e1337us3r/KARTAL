import csv,random,argparse

template_pool=[
"Context: #APP with 3 types of users #ACTOR, #ACTOR2 and #PRIVILAGED. #ACTOR and #ACTOR2 can only view and edit their own data. #PRIVILAGED can view and edit all data. Requests: [Request-1: #ACTOR-A GET /workshop/api/shop/orders with parameters orderID='#ACTOR-A';Response-1: OK with parameters orderID='#ACTOR-A',totalPrice=12,items.1.name='ball',items.2.price=1;Request-2: #ACTOR-B GET /workshop/api/shop/orders with parameters orderID='#ACTOR-B';Response-2: OK with parameters orderID='#ACTOR-B',totalPrice=155,items.1.name='hand',items.2.price=55;Request-3: #ACTOR-A GET /workshop/api/shop/orders with parameters orderID='#ACTOR-B';Response-3: OK with parameters orderID='#ACTOR-B',totalPrice=155,items.1.name='hand',items.2.price=55]",
"Context: #APP with 1 type of users #ACTOR, where they can book their own flights. Requests: [Request-1: #ACTOR-A POST /api/flights with parameters from='New York', to='Paris', date='2024-06-01'; Response-1: OK with parameters flightID='123', from='New York', to='Paris',date='2024-06-01', price=1200; Request-2: #ACTOR-B POST /api/flights with parameters from='San Francisco', to='Tokyo', date='2024-06-15'; Response-2: OK with parameters flightID='456', from='San Francisco', to='Tokyo',date='2024-06-15', price=2000; Request-3: #ACTOR-A DELETE /api/flights with parameters flightID='456'; Response-3: OK with parameters]",
"Context: #APP with 2 type of users #ACTOR and #PRIVILAGED,where #PRIVILAGED can view and update #ACTOR details for their own department. Requests: [Request-1: #PRIVILAGED-A GET /#ACTORs with parameters departmentID='A';Response-1: OK with parameters #ACTOR-ID='Emp-123', name='John Doe', designation='Software Engineer', salary=5000;Request-2: #PRIVILAGED-B GET /#ACTORs with parameters departmentID='B';Response-2: OK with parameters #ACTOR-ID='Emp-456', name='Jane Doe', designation='Business Analyst', salary=6000;Request-3: #PRIVILAGED-B PUT /#ACTORs with parameters #ACTOR-ID='Emp-123', salary=5500;Response-3: OK with parameters message='Salary updated successfully']",
"Context: #APP with 2 type of users #ACTOR and #PRIVILAGED, where #ACTORs can view and manage their own healthcare records. Requests: [Request-1: #ACTOR-A GET /healthcare with parameters #ACTORID='#ACTOR-A';Response-1: OK with parameters #ACTORID='#ACTOR-A', prescriptions=['Medicine A', 'Medicine B'], pastAppointments=[{'#PRIVILAGED': 'Dr. Johnson', 'Date': '05-05-2023'}, {'#PRIVILAGED': 'Dr. Smith', 'Date': '10-10-2023'}];Request-2: #ACTOR-B GET /healthcare with parameters #ACTORID='#ACTOR-B';Response-2: OK with parameters #ACTORID='#ACTOR-B', prescriptions=['Medicine C', 'Medicine D'], pastAppointments=[{'#PRIVILAGED': 'Dr. Williams', 'Date': '06-06-2023'}, {'#PRIVILAGED': 'Dr. Brown', 'Date': '12-12-2023'}];Request-3: #ACTOR-A POST /healthcare with parameters #ACTORID='#ACTOR-B', prescription='Medicine C';Response-3: OK with parameters message='Prescription added successfully']",
"Context: #APP with 2 type of users #ACTOR and #PRIVILAGED, where each #ACTOR can only view and download their own files. #PRIVILAGEDs cannot view #ACTOR files. Requests: [Request-1: #ACTOR-A GET /api/files with parameters fileID='#ACTOR-A/email.docx';Response-1: OK with parameters fileID='#ACTOR-A/email.docx',content='Hello World!',size=12KB;Request-2: #ACTOR-B GET /api/files with parameters fileID='#ACTOR-B/photos/beach.jpg';Response-2: OK with parameters fileID='#ACTOR-B/photos/beach.jpg', content ['...'],size=2MB;Request-3: #ACTOR-A POST /api/files with parameters fileContent='New Content';Response-3: OK with parameters fileID='#ACTOR-A/email.docx',content='New Content',size=10KB;Request-4: #ACTOR-B POST /api/files with parameters fileContent='New Content';Response-4: OK with parameters fileID='#ACTOR-B/photos/beach.jpg',content='New Content',size=1.5MB;Request-5: #PRIVILAGED GET /api/files with parameters fileID='#ACTOR-A/email.docx';Response-5: OK with parameters fileID='#ACTOR-A/email.docx',content='Hello World!',size=12KB]",
"Context: #APP with 2 type of users #ACTOR and #PRIVILAGED where each #ACTOR can only access and modify their own orders. #PRIVILAGED can view all orders. Requests: [Request-1: #ACTOR-A GET /api/orders with parameters orderID='Order-A';Response-1: OK with parameters orderID='Order-A',menu=['pizza','coke'],status='Delivered';Request-2: #ACTOR-B GET /api/orders with parameters orderID='Order-A';Response-2: OK with parameters orderID='Order-A',menu=['pizza','coke'],status='Completed';Request-3: #ACTOR-A PUT /api/orders with parameters status='Refunded';Response-3: OK with parameters orderID='Order-A',menu=['pizza','coke'],status='Refunded';Request-4: #ACTOR-B PUT /api/orders with parameters orderID='Order-A',status='Delivered';Response-4: Created with parameters orderID='Order-A',menu=['pizza','coke'],status='Delivered';Request-5: #PRIVILAGED GET /api/orders with parameters orderID='Order-A';Response-5: OK with parameters orderID='Order-A',menu=['pizza','coke'],status='Delivered']",
"Context: #APP with 2 type of users #ACTOR and #PRIVILAGED for advertisements where each #ACTOR can only see their own listings. #PRIVILAGEDs can view and delete all listings. Requests: [Request-1: #ACTOR-A Patch /market/#ACTOR/[#ACTOR-A-id]/items/[#ACTOR-A-itemId] with parameters name='Item-A';Response-1: OK with parameters itemId='#ACTOR-A-itemId',name='Item-A',price=10.5,quantity=103;Request-2: #ACTOR-A Get /market/#ACTOR/[#ACTOR-A-id]/items/[#ACTOR-B-itemId] with parameters;Response-2: OK with parameters itemId='#ACTOR-B-itemId',name='Item-B',price=303.8,quantity=52;]",
"Context: #APP where reviews and ratings are given for specific businesses but #ACTORs should not be able to modify others' reviews.Request-1: #ACTOR-A POST /api/business/123/review with parameters rating=4, comment='Nice place';Response-1: OK with parameters reviewID='Review-1234',businessID='Business-123',#ACTORID='#ACTOR-A',rating=4,comment='Nice place';Request-2: #ACTOR-B POST /api/business/123/review with parameters rating=2, comment='Terrible place, poor customer service';Response-2: OK with parameters reviewID='Review-2345',businessID='Business-123',#ACTORID='#ACTOR-B',rating=2,comment='Terrible place, poor customer service';Request-3: #ACTOR-A PUT /api/business/123/review with parameters reviewID='Review-2345',rating=1;Response-3: OK with parameters message='Review updated successfully’",
"Context: #APP with 3 type of users #ACTORs, #ACTOR2s and #PRIVILAGED. The #ACTORs can create posts and see their own published/unpublished articles. #ACTOR2s can edit their own posts and all #ACTORs' posts, but cannot change the status of the posts. #PRIVILAGEDs can edit anyone's articles and set the status for each one.;Request-1: #ACTOR-A GET /api/posts;Response-1: OK with parameters posts=['Post-1', 'Post-2'];Request-2: #ACTOR2-A GET /api/posts;Response-2: OK with parameters posts=['Post-1', 'Post-2', 'Post-3'];Request-3: #ACTOR2-B PATCH /api/posts with parameters postID='Post-2',content='Updated Content',status='drafted';Response-3: OK with parameters postID='Post-2',content='Updated Content', status='drafted';Request-4: #PRIVILAGED PATCH /api/posts with parameters postID='Post-2',content='Another Updated Content',status='published';Response-4: OK with parameters postID='Post-2',content='Another Updated Content', status='published’]",
"Context: #APP in which #ACTORs can share files with other #ACTORs or public. Only the owner of a file should be able to modify its attributes.;Request-1: #ACTOR-A POST /api/files with parameters content='Example content', access=public;Response-1: OK with parameters url='/files/public/12345/';Request-2: #ACTOR-B GET /api/files with parameters fileId='12345';Response-2: OK with parameters content='Example content', access=public;Request-3: #ACTOR-B PUT /api/files with parameters fileId='12345', content='Modified content';Response-3: 200 Ok with parameters fileId='12345',content='Modified content',access=public;Request-4: #ACTOR-A PUT /api/files with parameters fileId='12345', access=private;Response-4: OK with parameters url='/files/private/12345/';Request-5: #ACTOR-B GET /api/files with parameters fileId='12345';Response-5: Not Found with parameters errorCode=404,errorMessage='The file was not found.'",
]
app_pool=["A hotel booking system","An online file sharing app","An inventory management system","A school management system","A social networking app","an ecommerce app","A voting app","A messaging app","An online payment system","A network service","a banking web application","a task management tool","a database system","a hotel reservation","a file sharing system","an stats dashboard for a mobile app","A web app for ordering food online","A flight booking portal","A hobby social network","a supply chain management system","a website that provides links to external sources","An online course platform","A Sales reporting website"]
actor_pool=["Customer","User","Student","Person","Engineer","Developer","Clerk","Worker","Player","Audience","Member","Traveller","Consumer","Employee"]
privilaged_actor_pool=["Manager","Admin","Privilaged-User","Boss","Expert","Editor","Moderator","Seller","Executive","Owner"]
api_pool=["/","/content","/drive","/store","/view","/open","/folder","/system","/v1","/external","/service","/push","/backend","/server","/bff","/graph","/integration"]

def multiplier_generator(count):
    examples=[]
    for _ in range(count):
        for template_empty in template_pool:
            template = template_empty
            template=template.replace("#APP", app_pool[random.randint(0,len(app_pool)-1)])
            template=template.replace("#ACTOR", actor_pool[random.randint(0,len(actor_pool)-1)])
            template=template.replace("#ACTOR2", actor_pool[random.randint(0,len(actor_pool)-1)])
            template=template.replace("#PRIVILAGED", privilaged_actor_pool[random.randint(0,len(privilaged_actor_pool)-1)])
            template=template.replace("/api", api_pool[random.randint(0,len(api_pool)-1)]+api_pool[random.randint(0,len(api_pool)-1)])
            examples.append([template,1])
    return examples

def saveToFile(data, filename, write_headers=False):
    with open(filename, "a") as csvfile:
        writer = csv.writer(
            csvfile, delimiter="|", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        if write_headers:
            writer.writerow(["prompt", "labels"])
        writer.writerows(data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("outputfile",type=str)
    parser.add_argument("count",type=int)
    args = parser.parse_args()

    print(f"Generating {args.count*len(template_pool)} examples...")
    data=multiplier_generator(int(args.count))
    print(f"Saving to file {args.outputfile}...")
    saveToFile(data,args.outputfile)
    print("Done!")


if __name__ == "__main__":
    main()
