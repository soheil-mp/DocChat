# Database Schema Migration Guide

## Current Schema (v2.x)

### Documents Collection
    {
      _id: ObjectId,
      title: String,
      file_path: String,
      file_type: String,
      status: String,
      metadata: {
        created_at: DateTime,
        updated_at: DateTime,
        size: Number,
        chunks: Number
      },
      embeddings: {
        model: String,
        status: String,
        last_updated: DateTime
      }
    }

### Conversations Collection
    {
      _id: ObjectId,
      user_id: ObjectId,
      title: String,
      messages: [{
        role: String,
        content: String,
        timestamp: DateTime,
        references: [{
          document_id: ObjectId,
          chunk_id: String,
          relevance: Number
        }]
      }],
      metadata: {
        created_at: DateTime,
        updated_at: DateTime,
        model: String
      }
    }

## Migration Scripts

### Forward Migration
    # Update document schema
    db.documents.update({}, {
      $set: {
        "metadata.chunks": 0,
        "embeddings": {
          "model": "default",
          "status": "pending",
          "last_updated": null
        }
      }
    }, {multi: true})

### Rollback Scripts
    # Revert document schema
    db.documents.update({}, {
      $unset: {
        "metadata.chunks": "",
        "embeddings": ""
      }
    }, {multi: true}) 